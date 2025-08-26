from peewee import (
    Check,
    CompositeKey,
    DateTimeField,
    FloatField,
    ForeignKeyField,
    IntegerField,
    PrimaryKeyField,
    TextField,
)

from ycaro_airlines_v2.models.base_model import BaseModel


class City(BaseModel):
    name = TextField(constraints=[Check("Length(name) > 3")])


class Route(BaseModel):
    origin = ForeignKeyField(model=City)
    departure = ForeignKeyField(model=City)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        indexes = (
            (
                (
                    "origin",
                    "departure",
                ),
                True,
            ),
        )


class Seat(BaseModel):
    status = FieldEnum


class Flight(BaseModel):
    capacity = IntegerField(constraints=[Check("capacity > 0")], null=False)
    route = ForeignKeyField(model=Route)
    departure = DateTimeField()
    price = FloatField(constraints=[Check("price > 0")], null=False)
