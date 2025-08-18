from itertools import count
from typing import Self
from ycaro_airlines.models.booking import Booking


class Customer:
    customer_counter = count()
    customers: dict[int, Self] = {}

    def __init__(self, username: str) -> None:
        if username == "":
            raise ValueError("Username must be filled")

        self.username: str = username
        self.id: int = next(self.customer_counter)
        self.customers[self.id] = self
        self.loyalty_points = 0

    @property
    def bookings(self):
        return {k: v for k, v in Booking.bookings.items() if v.owner_id == self.id}

    @classmethod
    def get(cls, customer_id: int):
        return cls.customers.get(customer_id)

    @classmethod
    def get_by_username(cls, customer_username: str):
        for v in cls.customers.values():
            if v.username == customer_username:
                return v
        return None

    def gain_loyalty_points(self, amount: int):
        self.loyalty_points += amount

    def spend_loyalty_points(self, amount: int):
        self.loyalty_points -= amount
