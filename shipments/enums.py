import enum


@enum.unique
class BaseEnum(enum.Enum):

    @classmethod
    def choices(cls):
        return (tuple((i.name, i.value) for i in cls))


class ShipmentStatusEnum(str, BaseEnum):
    PROCCESSING = 'proccessing'
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    IN_PROGRESS = 'in_progress'
    DELIVERED = 'delivered'
    PENDING_CANCELATION = 'pending-cancelation'
    CANCELED = 'canceled'


class DimensionUnitsEnum(str, BaseEnum):
    CM = 'cm'
    Inch = 'in'


class WeightUnitsEnum(str, BaseEnum):
    KG = 'kg'
    Pound = 'lb'
