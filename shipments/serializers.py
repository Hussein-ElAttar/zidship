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

    class Meta:
        model = Shipment
        fields = '__all__'
        read_only_fields =('tracking_id', )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['courier'] = CourierSerializer(instance.courier).data
        response['status'] = ShipmentStatusSerializer(instance.status).data
        response['shipment_method'] = ShipmentMethodSerializer(instance.shipment_method).data
        return response
