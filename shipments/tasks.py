from zidship.celery import app

from shipments.models import Shipment
from shipments.services.factory_shipment_gateway import FactoryShipmentGateway


@app.task
def cancel_shipment_task(shipment_id):
    shipment = Shipment.objects.get(pk=shipment_id)
    shipment_gateway = FactoryShipmentGateway.get_shipment_gateway(shipment)
    shipment_gateway.cancel_shipment()


@app.task
def create_shipment_task(shipment_id):
    shipment = Shipment.objects.filter(id=shipment_id).get()
    shipment_gateway = FactoryShipmentGateway.get_shipment_gateway(shipment)
    shipment.tracking_id = shipment_gateway.create_waybill().tracking_id
    shipment.save()
