from core.exceptions import CoreException


class ShipmentException(CoreException):
    pass


class ShipmentAlreadyCanceled(ShipmentException):
    status_code = 400
    default_detail = 'Shipment cancelation is already requested.'


class ShipmentCouldNotBeCreated(ShipmentException):
    status_code = 500
    default_detail = 'The requested shipment could not be created.'


class ShipmentCouldNotBeCanceled(ShipmentException):
    status_code = 500
    default_detail = 'The requested shipment could not be canceled.'


class ShipmentCouldNotBeTracked(ShipmentException):
    status_code = 500
    default_detail = 'The requested shipment could not be tracked.'


class ShipmentCouldNotBePrinted(ShipmentException):
    status_code = 500
    default_detail = 'The requested shipment could not be printed.'
