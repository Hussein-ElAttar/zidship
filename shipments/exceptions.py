from rest_framework.exceptions import APIException

class ShipmentCouldNotBeCreated(APIException):
    status_code = 500
    default_detail = 'The requested shipment could not be created.'

class ShipmentCouldNotBeCanceled(APIException):
    status_code = 500
    default_detail = 'The requested shipment could not be canceled.'

class ShipmentCouldNotBeTracked(APIException):
    status_code = 500
    default_detail = 'The requested shipment could not be tracked.'


class ShipmentCouldNotBePrinted(APIException):
    status_code = 500
    default_detail = 'The requested shipment could not be printed.'
