from enum import Enum, auto
from itertools import count
from typing import Self
from ycaro_airlines.models.flight import Flight, stringify_date
from rich.table import Table
from rich.console import Console


class BookingStatus(Enum):
    booked = 1
    checked_in = auto()
    cancelled = auto()


type customer_id = int


class Booking:
    booking_counter = count()
    bookings: dict[int, Self] = {}

    def __init__(
        self,
        flight: Flight,
        customer_id: customer_id,
        passenger_name: str,
        passenger_cpf: str,
    ):
        self.flight = flight
        self.id = next(self.booking_counter)
        self.owner_id = customer_id
        self.price = self.flight.price
        self.status = BookingStatus.booked
        self.seat_id: int | None = None
        self.bookings[self.id] = self
        self.passenger_name = passenger_name
        self.passenger_cpf = passenger_cpf

    def cancel_booking(self):
        self.status = BookingStatus.cancelled

        if self.seat_id:
            self.flight.open_seat(self.seat_id)

    @property
    def seat(self):
        return self.flight.seats[self.seat_id] if self.seat_id else None

    @classmethod
    def list_bookings(cls, customer_id: customer_id):
        return list(
            filter(
                lambda x: True if x.owner_id == customer_id else False,
                cls.bookings.values(),
            )
        )

    def check_in(self) -> bool:
        if self.seat_id is None:
            print("Booking seat not chosen")
            return False

        if not self.flight.check_in_seat(self.id, self.seat_id):
            return False

        self.status = BookingStatus.checked_in

        return True

    def reserve_seat(self, seat_id: int) -> bool:
        reserved_seat = self.flight.occupy_seat(booking_id=self.id, seat_id=seat_id)

        if reserved_seat is None:
            return False

        if self.seat_id:
            self.flight.open_seat(self.seat_id)

        self.seat_id = reserved_seat.id
        return True

    @classmethod
    def print_bookings_table(cls, customer_id: customer_id, console: Console):
        table = Table(title="Bookings")
        table.add_column("Booking")
        table.add_column("Flight")
        table.add_column("From", justify="right", no_wrap=True)
        table.add_column("Departure", justify="right", no_wrap=True)
        table.add_column("Destination")
        table.add_column("Arrival", justify="right", no_wrap=True)
        table.add_column("Status", justify="right", no_wrap=True)
        table.add_column("Seat", justify="right", no_wrap=True)

        for i in cls.list_bookings(customer_id):
            table.add_row(
                f"{i.id}",
                f"{i.flight.id}",
                f"{i.flight.From}",
                f"{stringify_date(i.flight.departure)}",
                f"{i.flight.To}",
                f"{stringify_date(i.flight.arrival)}",
                f"{i.status.name}",
                f"{i.seat_id}" if i.seat_id else "N/A",
            )

        console.print(table)

    def print_booking_table(self, console: Console):
        pass
