from rest_framework import serializers

from shipments.models import Courier, Shipment, ShipmentStatus

from .models import ShipmentMethod


class CourierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = '__all__'


class ShipmentMethodSerializer(serializers.ModelSerializer):
    courier = CourierSerializer(read_only=True)

    class Meta:
        model = ShipmentMethod
        fields = '__all__'


class ShipmentStatusSerializer(serializers.ModelSerializer):
    courier = CourierSerializer(read_only=True)

    class Meta:
        model = ShipmentStatus
        fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    status = ShipmentStatusSerializer(read_only=True)
    courier = CourierSerializer(read_only=True)
    shipment_method = ShipmentMethodSerializer(read_only=True)

    class Meta:
        model = Shipment
        fields = '__all__'
