from abc import ABC

from shipments.models import Shipment

from .abstract_shipment_gateway import AbstractShipmentGateway
from .fedex_shipment_gatway import FedexShipmentGateway


class FactoryShipmentGateway(ABC):
    gateways = {
        1: FedexShipmentGateway,
    }

    @classmethod
    def get_shipment_gateway(cls, shipment: Shipment) -> AbstractShipmentGateway:
        Gateway = cls.gateways.get(shipment.courier.id, None)

        if(Gateway is None):
            return None

        return Gateway(shipment=shipment)
