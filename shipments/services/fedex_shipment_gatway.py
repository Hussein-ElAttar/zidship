import uuid

from shipments.enums import ShipmentStatusEnum
from shipments.exceptions import (ShipmentCouldNotBeCanceled,
                                  ShipmentCouldNotBeCreated,
                                  ShipmentCouldNotBePrinted,
                                  ShipmentCouldNotBeTracked)

from .abstract_shipment_gateway import (AbstractShipmentGateway,
                                        CreateWaybillMapping,
                                        TrackShipmentMapping)


class FedexShipmentGateway(AbstractShipmentGateway):

    def create_waybill(self) -> CreateWaybillMapping:
        try:
            tracking_id = str(uuid.uuid4())
        except:
            raise ShipmentCouldNotBeCreated
        else:
            return CreateWaybillMapping(tracking_id=tracking_id)

    def track_shipment(self) -> list[TrackShipmentMapping]:
        try:
            track_shipment_arrays = []
            track_shipment_arrays.append(TrackShipmentMapping(location='Alexandria', description='Shipment picked up'))
            track_shipment_arrays.append(TrackShipmentMapping(location='Alexandria', description='Shipment arrived at facility'))
            track_shipment_arrays.append(TrackShipmentMapping(location='Cairo', description='Shipment arrived at facility'))
        except:
            raise ShipmentCouldNotBeTracked
        else:
            return track_shipment_arrays

    def cancel_shipment(self) -> bool:
        try:
            self.shipment.status = ShipmentStatusEnum.CANCELED
            self.shipment.save()
        except:
            raise ShipmentCouldNotBeCanceled
        else:
            return True

    def print_waybill(self):
        try:
            self.shipment.status = ShipmentStatusEnum.CANCELED
            self.shipment.save()
        except:
            raise ShipmentCouldNotBePrinted
        else:
            return True
