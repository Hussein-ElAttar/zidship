import uuid

from django.template.loader import render_to_string
from shipments.enums import ShipmentStatusEnum
from shipments.exceptions import (ShipmentAlreadyCanceled,
                                  ShipmentCouldNotBeCanceled,
                                  ShipmentCouldNotBeCreated,
                                  ShipmentCouldNotBePrinted,
                                  ShipmentCouldNotBeTracked)
from shipments.services.abstract_shipment_gateway import PrintWaybillMapping
from weasyprint import HTML

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
        if(self.shipment.status.status in [ShipmentStatusEnum.PENDING_CANCELATION, ShipmentStatusEnum.CANCELED]):
            raise ShipmentAlreadyCanceled

        try:
            self.shipment.status = self.shipment.courier.shipmentstatus_courier.filter(status=ShipmentStatusEnum.PENDING_CANCELATION).get()
            self.shipment.save()
    
            # TODO:: Use workers here
            self.shipment.status = self.shipment.courier.shipmentstatus_courier.filter(status=ShipmentStatusEnum.CANCELED).get()
            self.shipment.save()

        except Exception as e:
            print(e)
            raise ShipmentCouldNotBeCanceled
        else:
            return self.shipment

    def print_waybill(self):
        try:
            html_string = render_to_string('shipments/fedex_label.html', context={'shipment': self.shipment})
            html = HTML(string=html_string)
            pdf_file = html.write_pdf()
        except:
            raise ShipmentCouldNotBePrinted
        else:
            return PrintWaybillMapping(file=pdf_file)

