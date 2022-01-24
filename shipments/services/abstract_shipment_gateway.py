import uuid
from abc import ABC, abstractmethod

from shipments.models import Courier, Shipment


class TrackShipmentMapping():
    location: str = None
    description: str = None

    def __init__(self, *args, **kwargs):
        self.location = kwargs['location']
        self.description = kwargs['description']


class CreateWaybillMapping():
    tracking_id: str = None

    def __init__(self, *args, **kwargs):
        self.tracking_id = kwargs['tracking_id']

class AbstractShipmentGateway(ABC):
    """ Logic for each third party integration should be implemented in the derived class """
    shipment: Shipment = None
    courier: Courier = None

    def __init__(self, *args, **kwargs):
        self.shipment = kwargs['shipment']
        self.courier = self.shipment.courier

    @abstractmethod
    def create_waybill(self) -> CreateWaybillMapping:

        return CreateWaybillMapping(tracking_id=str(uuid.uuid4()))

    @abstractmethod
    def print_waybill(self):
        pass

    @abstractmethod
    def track_shipment(self) -> list[TrackShipmentMapping]:
        pass

    @abstractmethod
    def cancel_shipment(self) -> bool:
        pass
