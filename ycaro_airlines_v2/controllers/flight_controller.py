from datetime import datetime
from typing import NotRequired, TypedDict

from ycaro_airlines_v2.models.flight import Flight


class FlightQueryParams(TypedDict):
    date_arrival_gte: NotRequired[datetime]
    date_departure_gte: NotRequired[datetime]

    date_arrival_lte: NotRequired[datetime]
    date_departure_lte: NotRequired[datetime]

    price_lte: NotRequired[float]
    price_gte: NotRequired[float]

    city_from: NotRequired[str]
    city_to: NotRequired[str]

    flight_id: NotRequired[int]


class FlightController:
    @staticmethod
    def list_flights(*query, **filters):
        return Flight.select(**filters).where(*query)
