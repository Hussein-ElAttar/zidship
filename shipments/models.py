from django.db import models

from shipments.enums import DimensionUnits, ShipmentStatus, WeightUnits


class Courier(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)


class Shipment(models.Model):
    courier = models.ForeignKey('shipments.courier', on_delete=models.CASCADE, related_name="%(class)s_courier")
    status = models.ForeignKey('shipments.shipmentStatus', on_delete=models.CASCADE, related_name="%(class)s_courier")
    tracking_id = models.CharField(null=True, max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    weight_unit = models.CharField(choices=DimensionUnits.choices(), max_length=15, default=WeightUnits.KG)
    height = models.DecimalField(max_digits=6, decimal_places=2),
    width = models.DecimalField(max_digits=6, decimal_places=2),
    length = models.DecimalField(max_digits=6, decimal_places=2),
    dimensions_unit = models.CharField(choices=DimensionUnits.choices(), max_length=15, default=DimensionUnits.CM)
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
    pickup_date = models.DateTimeField(null=True),
    estimated_delivery_date = models.DateTimeField(null=True),


class ShipmentMethods(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


class ShipmentStatus(models.Model):
    status = models.CharField(choices=ShipmentStatus.choices(),max_length=100, default=ShipmentStatus.PENDING, db_index=True)
    courier = models.ForeignKey('shipments.courier', on_delete=models.CASCADE, related_name="%(class)s_courier")
    source_id = models.CharField(null=True, max_length=200)
    source_description = models.TextField(blank=True, null=True)
