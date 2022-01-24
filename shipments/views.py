from rest_framework import status, viewsets
from rest_framework.response import Response

from shipments.models import Courier, Shipment, ShipmentStatus
from shipments.serializers import (CourierSerializer, ShipmentSerializer,
                                   ShipmentStatusSerializer)

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


# TODO:: Use strategy pattern with a shipment service
class ShipmentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """
    `list` and `retrieve` Courier actions.
    """
    queryset = ShipmentMethod.objects.all()
    serializer_class = ShipmentMethodSerializer


# TODO:: Use strategy pattern with a shipment service
class ShipmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Shipment.objects.all()
    lookup_field = 'tracking_id'
    serializer_class = ShipmentSerializer
    filterset_fields = ['courier', 'tracking_id']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
