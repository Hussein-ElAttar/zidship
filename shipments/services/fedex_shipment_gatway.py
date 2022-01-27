import json
import uuid
from typing import List

import requests
from django.template.loader import render_to_string
from shipments.enums import ShipmentStatusEnum
from shipments.exceptions import (ShipmentAlreadyCanceled,
                                  ShipmentCouldNotBeCanceled,
                                  ShipmentCouldNotBeCreated,
                                  ShipmentCouldNotBePrinted,
                                  ShipmentCouldNotBeTracked)
from shipments.models import CourierApiSettings, Shipment
from shipments.services.abstract_shipment_gateway import PrintWaybillMapping
from shipments.services.oauth2_api_gateway import OAuth2ApiGateway
from weasyprint import HTML

from .abstract_shipment_gateway import (AbstractShipmentGateway,
                                        CreateWaybillMapping,
                                        TrackShipmentMapping)

"""
    Only create way_bill() is calling the real fedex api,
    the rest of the methods down below are just for demonestration and should also be calling it if needed
"""
class FedexShipmentGateway(AbstractShipmentGateway):
    api_gateway_service: OAuth2ApiGateway = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        courier_api_settings = CourierApiSettings.objects.filter(
            courier=self.shipment.courier).get()
        self.api_gateway_service = OAuth2ApiGateway(courier_api_settings)

    def create_waybill(self) -> CreateWaybillMapping:
        try:
            self.api_gateway_service.authenticate()

            url = self.api_gateway_service.settings.api_url + '/ship/v1/shipments/'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.api_gateway_service.get_access_token()
            }

            response = requests \
                .post(url, json=self.get_create_waybill_request_mock(), headers=headers) \
                .json()

            tracking_id = response['output']['transactionShipments'][0]['masterTrackingNumber']
            self.shipment.tracking_id = tracking_id
            self.shipment.save()

        except Exception as e:
            print(e)
            raise ShipmentCouldNotBeCreated
        else:
            return CreateWaybillMapping(tracking_id=tracking_id)

    # Dummy data
    def track_shipment(self) -> List[TrackShipmentMapping]:
        try:
            if(self.shipment.status.code == ShipmentStatusEnum.PROCCESSING):
                return [TrackShipmentMapping(location='', description='Shipment is still proccessing')]

            track_shipment_arrays = []
            track_shipment_arrays.append(TrackShipmentMapping(
                location='Alexandria', description='Shipment picked up'))
            track_shipment_arrays.append(TrackShipmentMapping(
                location='Alexandria', description='Shipment arrived at facility'))
            track_shipment_arrays.append(TrackShipmentMapping(
                location='Cairo', description='Shipment arrived at facility'))
        except:
            raise ShipmentCouldNotBeTracked
        else:
            return track_shipment_arrays

    def cancel_shipment(self) -> Shipment:
        try:
            self.shipment.status = self.shipment.courier.shipmentstatus_courier \
                .filter(code=ShipmentStatusEnum.CANCELED).get()
            self.shipment.save()

        except Exception as e:
            print(e)
            raise ShipmentCouldNotBeCanceled
        else:
            return self.shipment

    def print_waybill(self):
        try:
            html_string = render_to_string(
                'shipments/fedex_label.html',
                context={'shipment': self.shipment}
            )
            html = HTML(string=html_string)
            pdf_file = html.write_pdf()
        except:
            raise ShipmentCouldNotBePrinted
        else:
            return PrintWaybillMapping(file=pdf_file)

    def is_shipment_cancable(self, raise_exception=True):
        if(self.shipment.status.code in [ShipmentStatusEnum.PENDING_CANCELATION, ShipmentStatusEnum.CANCELED]):
            raise ShipmentAlreadyCanceled

    def is_valid_shipment(self, raise_exception=True):
        return True

    """ 
        This is just a mock for demosteration purposes. In reality, all fields should be mapped properly from the model
        Just like the address fields down below
    """
    def get_create_waybill_request_mock(self):
        return {
            "labelResponseOptions": "URL_ONLY",
            "requestedShipment": {
                "shipper": {
                    "contact": {
                        "personName": "SHIPPER NAME",
                        "phoneNumber": 1234567890,
                        "companyName": "Shipper Company Name"
                    },
                    "address": {
                        "streetLines": [
                            self.shipment.sender_address
                        ],
                        "city": "Memphis",
                        "stateOrProvinceCode": "TN",
                        "postalCode": 38116,
                        "countryCode": "US"
                    }
                },
                "recipients": [
                    {
                        "contact": {
                            "personName": "RECIPIENT NAME",
                            "phoneNumber": 1234567890,
                            "companyName": "Recipient Company Name"
                        },
                        "address": {
                            "streetLines": [
                                self.shipment.receiver_address
                            ],
                            "city": "RICHMOND",
                            "stateOrProvinceCode": "BC",
                            "postalCode": "V7C4V7",
                            "countryCode": "CA"
                        }
                    }
                ],
                "shipDatestamp": "2022-02-03",
                "serviceType": "INTERNATIONAL_PRIORITY",
                "packagingType": "YOUR_PACKAGING",
                "pickupType": "USE_SCHEDULED_PICKUP",
                "blockInsightVisibility": False,
                "shippingChargesPayment": {
                    "paymentType": "SENDER"
                },
                "labelSpecification": {
                    "imageType": "PDF",
                    "labelStockType": "PAPER_85X11_TOP_HALF_LABEL"
                },
                "customsClearanceDetail": {
                    "dutiesPayment": {
                        "paymentType": "SENDER"
                    },
                    "isDocumentOnly": True,
                    "commodities": [
                        {
                            "description": "Commodity description",
                            "countryOfManufacture": "US",
                            "quantity": 1,
                            "quantityUnits": "PCS",
                            "unitPrice": {
                                "amount": 100,
                                "currency": "USD"
                            },
                            "customsValue": {
                                "amount": 100,
                                "currency": "USD"
                            },
                            "weight": {
                                "units": "LB",
                                "value": 20
                            }
                        }
                    ]
                },
                "shippingDocumentSpecification": {
                    "shippingDocumentTypes": [
                        "COMMERCIAL_INVOICE"
                    ],
                    "commercialInvoiceDetail": {
                        "documentFormat": {
                            "stockType": "PAPER_LETTER",
                            "docType": "PDF"
                        }
                    }
                },
                "requestedPackageLineItems": [
                    {
                        "weight": {
                            "units": "LB",
                            "value": 70
                        }
                    }
                ]
            },
            "accountNumber": {
                "value": "740561073"
            }
        }
