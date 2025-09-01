from ycaro_airlines.models.booking import Booking
from ycaro_airlines.models.customer_service import Issue
from ycaro_airlines.models.model_database import ModelRepository
from ycaro_airlines.models.user import Roles, User


class Customer(User):
    def __init__(self, username: str, *args, **kwargs) -> None:
        role = Roles.Customer
        self.loyalty_points = 0

        super().__init__(username=username, role=role, *args, **kwargs)

    @property
    def bookings(self):
        return {k: v for k, v in Booking.bookings.items() if v.owner_id == self.id}

    @classmethod
    def get_by_username(cls, customer_username: str):
        for v in cls.repository.list():
            if v is None:
                continue

            if v.username == customer_username:
                return v

        return None

    @property
    def issues(self):
        return filter(
            lambda x: True if x.customer_id == self.id else False, Issue.list()
        )

    def gain_loyalty_points(self, amount: int):
        self.loyalty_points += amount

    def spend_loyalty_points(self, amount: int):
        self.loyalty_points -= amount


CustomerRepository = ModelRepository[Customer]()
