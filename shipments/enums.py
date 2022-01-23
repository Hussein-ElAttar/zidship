import enum


@enum.unique
class BaseEnum(enum.Enum):

    @classmethod
    def choices(cls):
        return (tuple((i.name, i.value) for i in cls))


class ShipmentStatus(str, BaseEnum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    IN_PROGRESS = 'in_progress'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'


class DimensionUnits(str, BaseEnum):
    CM = 'cm'
    Inch = 'in'


class WeightUnits(str, BaseEnum):
    KG = 'kg'
    Pound = 'lb'
