import uuid
from abc import ABC, abstractmethod
from typing import List

from shipments.exceptions import CourierDoesNotSupportCancel
from shipments.models import Courier, Shipment
from shipments.serializers import ShipmentSerializer


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


class PrintWaybillMapping():
    file = None
    filetype: str = None
    filename: str = None

    def __init__(self, *args, **kwargs):
        self.file = kwargs['file']
        self.filetype = 'application/pdf'
        self.filename = 'Waybill' + '-' + str(uuid.uuid4()) + '.pdf'


class AbstractShipmentGateway(ABC):
    """ Logic for each third party integration should be implemented in the derived class """
    shipment: Shipment = None
    courier: Courier = None
    serializer: ShipmentSerializer = ShipmentSerializer

    def __init__(self, *args, **kwargs):
        self.shipment = kwargs['shipment']
        self.courier = self.shipment.courier

    @abstractmethod
    def create_waybill(self) -> CreateWaybillMapping:
        pass

    @abstractmethod
    def print_waybill(self) -> PrintWaybillMapping:
        pass

    @abstractmethod
    def track_shipment(self) -> List[TrackShipmentMapping]:
        pass

    @abstractmethod
    def is_valid_shipment(self, raise_exception=True):
        pass

    def cancel_shipment(self) -> Shipment:
        self.is_shipment_cancable(raise_exception=True)

    def is_shipment_cancable(self, raise_exception=True):
        if(raise_exception):
            raise CourierDoesNotSupportCancel
        else:
            return False
