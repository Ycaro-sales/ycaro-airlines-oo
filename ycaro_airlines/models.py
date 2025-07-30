from datetime import datetime, timedelta
from functools import reduce
from random import randint, sample
from enum import Enum, auto
from itertools import count
from rich.table import Table
from rich.console import Console
from typing import Any, Callable, Optional, Self, TypeVar, Generic

cities = ["Maceio", "Recife", "Aracaju", "Joao Pessoa"]
T = TypeVar("T")


def stringify_date(date: datetime):
    return f"{str(date.hour).zfill(2)}:{str(date.minute).zfill(2)} {str(date.day).zfill(2)}/{str(date.month).zfill(2)}"


class Flight:
    flights: dict[int, Self] = {}
    flight_counter = count()

    def __init__(
        self,
        From: str,
        To: str,
        capacity: int = 255,
        departure: datetime = datetime.now() + timedelta(hours=1),
        arrival: datetime = datetime.now() + timedelta(hours=3),
        price: float = 200.00,
    ) -> None:
        self.From: str = From
        self.To: str = To
        self.id: int = next(self.flight_counter)
        self.capacity = capacity
        self.departure: datetime = departure
        self.arrival: datetime = arrival
        self.price: float = price
        self.seats: list["Booking | None"] = [None for _ in range(0, self.capacity)]

    def __str__(self):
        return f"{self.id} - {self.From} -> {self.To}\n{stringify_date(self.departure)} -> {stringify_date(self.arrival)} | R${self.price} "

    @classmethod
    def mock_flight(cls):
        """Creates mocked flights to fill flights global dictionary"""
        timedelta_arrival = timedelta(hours=randint(1, 5))
        city1, city2 = sample(cities, k=2)
        price = randint(100, 400)
        mock: Flight = Flight(
            From=city1,
            To=city2,
            departure=datetime.now() + timedelta_arrival,
            arrival=datetime.now() + timedelta_arrival + timedelta(hours=randint(1, 5)),
            price=price,
        )

        Flight.flights[mock.id] = mock
        return mock

    def check_in_booking(self, booking: "Booking"):
        if booking.seat is None:
            return

    # TODO: Implement reserve seat
    def reserve_seat(self, booking: "Booking", seat: int):
        if self.seats[seat] is not None:
            return False
        self.seats[seat] = booking

    @classmethod
    def list_flights(cls):
        return list(cls.flights.values())

    @classmethod
    def print_flights_table(
        cls, console: Console, filters: list[Callable[[list[Any]]]] | None = None
    ):
        # filtered_flights = cls.list_flights()
        # for filter in filters:
        #     filtered_flights = filter(filtered_flights)
        table = Table(title="Flights")
        table.add_column("Flight")
        table.add_column("From", justify="right", no_wrap=True)
        table.add_column("Departure", justify="right", no_wrap=True)
        table.add_column("Destination")
        table.add_column("Arrival", justify="right", no_wrap=True)
        table.add_column("Price", justify="right", no_wrap=True)

        for i in cls.list_flights():
            table.add_row(
                f"{i.id}",
                f"{i.From}",
                f"{stringify_date(i.departure)}",
                f"{i.To}",
                f"{stringify_date(i.arrival)}",
                "${:,.2f}".format(i.price),
            )

        console.print(table)

    def print_flight_table(self, console: Console):
        table = Table(title="Flights")
        table.add_column("Flight")
        table.add_column("From", justify="right", no_wrap=True)
        table.add_column("Departure", justify="right", no_wrap=True)
        table.add_column("Destination")
        table.add_column("Arrival", justify="right", no_wrap=True)
        table.add_column("Price", justify="right", no_wrap=True)

        table.add_row(
            f"{self.id}",
            f"{self.From}",
            f"{stringify_date(self.departure)}",
            f"{self.To}",
            f"{stringify_date(self.arrival)}",
            "${:,.2f}".format(self.price),
        )

        console.print(table)


class Customer:
    customer_counter = count()
    customers: dict[int, Self] = {}

    def __init__(self, username: str) -> None:
        self.username: str = username
        self.id: int = next(self.customer_counter)
        self.customers[self.id] = self

    @property
    def bookings(self):
        return {k: v for k, v in Booking.bookings.items() if v.owner == self}

    def list_bookings(self):
        return Booking.list_bookings(self)


class BookingStatus(Enum):
    booked = 1
    checked_in = auto()
    cancelled = auto()


class Booking:
    booking_counter = count()
    bookings: dict[int, Self] = {}

    def __init__(self, flight: Flight, customer: Customer):
        self.flight = flight
        self.id = next(self.booking_counter)
        self.owner = customer
        self.status = BookingStatus.booked
        self.seat = None
        self.bookings[self.id] = self

    def cancel_booking(self):
        self.status = BookingStatus.cancelled
        if self.seat:
            self.flight.seats[self.seat] = None

    @classmethod
    def list_bookings(cls, customer: Customer):
        return list(
            filter(
                lambda x: True if x.owner.id == customer.id else False,
                cls.bookings.values(),
            )
        )

    def check_in(self, seat: Optional[int] = None):
        self.status = BookingStatus.checked_in
        if self.seat is None and seat is not None:
            self.select_seat(seat)

    def select_seat(self, seat: int):
        self.seat = seat
        self.flight.check_in_booking(self)

    @classmethod
    def print_bookings_table(cls, customer: Customer, console: Console):
        table = Table(title="Bookings")
        table.add_column("Booking")
        table.add_column("Flight")
        table.add_column("From", justify="right", no_wrap=True)
        table.add_column("Departure", justify="right", no_wrap=True)
        table.add_column("Destination")
        table.add_column("Arrival", justify="right", no_wrap=True)
        table.add_column("Status", justify="right", no_wrap=True)

        for i in cls.list_bookings(customer):
            table.add_row(
                f"{i.id}",
                f"{i.flight.id}",
                f"{i.flight.From}",
                f"{stringify_date(i.flight.departure)}",
                f"{i.flight.To}",
                f"{stringify_date(i.flight.arrival)}",
                f"{i.status.name}",
            )

        console.print(table)

    def print_booking_table(self, console: Console):
        pass
