from enum import Enum, auto


class BookingStatus(Enum):
    booked = 1
    checked_in = auto()
    cancelled = auto()


type customer_id = int
