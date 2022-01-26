from core.models import TimestampedModel
from django.db import models

from shipments.enums import (DimensionUnitsEnum, ShipmentStatusEnum,
                             WeightUnitsEnum)


class Courier(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)


class Shipment(TimestampedModel):
    courier = models.ForeignKey('shipments.Courier', on_delete=models.CASCADE, related_name="%(class)s_courier")
    status = models.ForeignKey('shipments.ShipmentStatus', on_delete=models.CASCADE, related_name="%(class)s_status")
    shipment_method = models.ForeignKey('shipments.ShipmentMethod', on_delete=models.CASCADE, related_name="%(class)s_method")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="%(class)s_user")
    tracking_id = models.CharField(null=True, max_length=200)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    weight_unit = models.CharField(choices=WeightUnitsEnum.choices(), max_length=15, default=WeightUnitsEnum.KG)
    height = models.DecimalField(max_digits=6, decimal_places=2)
    width = models.DecimalField(max_digits=6, decimal_places=2)
    length = models.DecimalField(max_digits=6, decimal_places=2)
    dimensions_unit = models.CharField(choices=DimensionUnitsEnum.choices(), max_length=15, default=DimensionUnitsEnum.CM)
    sender_address = models.CharField(max_length=200)
    sender_country = models.CharField(max_length=200)
    sender_city = models.CharField(max_length=200)
    sender_postal_code = models.CharField(max_length=200)
    sender_phone_number = models.CharField(max_length=15)
    receiver_address = models.CharField(max_length=200)
    receiver_country = models.CharField(max_length=200)
    receiver_city = models.CharField(max_length=200)
    receiver_postal_code = models.CharField(max_length=15)
    receiver_phone_number = models.CharField(max_length=15)
    pickup_date = models.DateTimeField(null=True)
    estimated_delivery_date = models.DateTimeField(null=True)


class ShipmentMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    courier = models.ForeignKey('shipments.Courier', on_delete=models.CASCADE, related_name="%(class)s_courier")


class ShipmentStatus(models.Model):
    code = models.CharField(choices=ShipmentStatusEnum.choices(), max_length=100, default=ShipmentStatusEnum.PROCCESSING, db_index=True)
    courier = models.ForeignKey('shipments.Courier', on_delete=models.CASCADE, related_name="%(class)s_courier")
    description = models.TextField(blank=True, null=True)
    external_code = models.CharField(null=True, max_length=200)
    external_description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('code', 'courier', 'external_code')
