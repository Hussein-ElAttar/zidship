from core.renderers import ZidshipJSONRenderer
from django.db import transaction
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shipments.enums import ShipmentStatusEnum
from shipments.models import Courier, Shipment, ShipmentStatus
from shipments.serializers import (CourierSerializer, ShipmentSerializer,
                                   ShipmentStatusSerializer)
from shipments.services import FactoryShipmentGateway

from .models import ShipmentMethod
from .serializers import ShipmentMethodSerializer
from .tasks import cancel_shipment_task, create_shipment_task


class CourierViewSet(viewsets.ReadOnlyModelViewSet):
    """
    `list` and `retrieve` Courier actions.
    """
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = (IsAuthenticated,)


class ShipmentStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    `list` and `retrieve` Available ShipmentStatuses actions.
    """
    queryset = ShipmentStatus.objects.all()
    serializer_class = ShipmentStatusSerializer
    permission_classes = (IsAuthenticated,)


class ShipmentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """
    `list` and `retrieve` Courier actions.
    """
    queryset = ShipmentMethod.objects.all()
    serializer_class = ShipmentMethodSerializer
    permission_classes = (IsAuthenticated,)



class ShipmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ['courier']

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create Shipment."""
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shipment = serializer.save()

        # Validate with third party
        shipment_gateway = FactoryShipmentGateway.get_shipment_gateway(
            shipment)
        shipment_gateway.is_valid_shipment(raise_exception=True)

        # Task
        create_shipment_task.delay(shipment.id)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def print(self, request, *args, **kwargs):
        """Print pdf."""
        instance = self.get_object()
        shipment_gateway = FactoryShipmentGateway.get_shipment_gateway(
            instance)
        print_waybill_mapping = shipment_gateway.print_waybill()

        response = HttpResponse(
            print_waybill_mapping.file, content_type=print_waybill_mapping.filetype)
        response['Content-Disposition'] = f'filename="{print_waybill_mapping.filename}"'
        return response

    def track(self, request, *args, **kwargs):
        """Track Shipment."""
        instance = self.get_object()
        shipment_gateway = FactoryShipmentGateway.get_shipment_gateway(
            instance)

        locations = [loc.__dict__ for loc in shipment_gateway.track_shipment()]

        return Response(locations)

    def cancel(self, request, *args, **kwargs):
        """Cancel Shipment if applicable"""
        shipment = self.get_object()
        shipment_gateway = FactoryShipmentGateway.get_shipment_gateway(
            shipment)
        shipment_gateway.is_shipment_cancable(raise_exception=True)

        shipment.status = shipment.courier.shipmentstatus_courier.filter(
            code=ShipmentStatusEnum.PENDING_CANCELATION).get()
        shipment.save()

        # Task
        cancel_shipment_task.delay(shipment.id)

        serializer = self.get_serializer(shipment)

        return Response(serializer.data)
