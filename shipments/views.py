from django.db import transaction
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response

from shipments.enums import ShipmentStatusEnum
from shipments.models import Courier, Shipment, ShipmentStatus
from shipments.serializers import (CourierSerializer, ShipmentSerializer,
                                   ShipmentStatusSerializer)
from shipments.services import FactoryShipmentGateway

from .models import ShipmentMethod
from .serializers import ShipmentMethodSerializer


class CourierViewSet(viewsets.ReadOnlyModelViewSet):
    """
    `list` and `retrieve` Courier actions.
    """
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer


class ShipmentStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    `list` and `retrieve` Available ShipmentStatuses actions.
    """
    queryset = ShipmentStatus.objects.all()
    serializer_class = ShipmentStatusSerializer


class ShipmentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """
    `list` and `retrieve` Courier actions.
    """
    queryset = ShipmentMethod.objects.all()
    serializer_class = ShipmentMethodSerializer


class ShipmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    filterset_fields = ['courier']

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # TODO:: Use workers here
        shipment_gateway = FactoryShipmentGateway.get_shipment_gateway(instance)
        tracking_id = shipment_gateway.create_waybill()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def print(self, request, *args, **kwargs):
        """Print pdf."""
        instance = self.get_object()
        shipment_gateway = FactoryShipmentGateway.get_shipment_gateway(instance)
        print_waybill_mapping = shipment_gateway.print_waybill()

        response = HttpResponse(print_waybill_mapping.file, content_type=print_waybill_mapping.filetype)
        response['Content-Disposition'] = f'filename="{print_waybill_mapping.filename}"'
        return response


    def cancel(self, request, *args, **kwargs):
        """Cancel Shipment"""
        instance = self.get_object()

        # TODO:: Use workers here
        shipment_gateway = FactoryShipmentGateway.get_shipment_gateway(instance)
        shipment = shipment_gateway.cancel_shipment()
        serializer = self.get_serializer(shipment)

        return Response(serializer.data)
