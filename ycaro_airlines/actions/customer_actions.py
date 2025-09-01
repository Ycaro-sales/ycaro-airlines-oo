import questionary
from ycaro_airlines.models.booking import Booking
from ycaro_airlines.models.user import User


def create_special_requests_action(user: User, Booking: Booking):
    questionary.confirm(
        "do you need any special requests?(accessibility, foods, other)"
    ).ask()
    questionary.checkbox(
        "What do you wish to request?",
        choices=["accessibility", "dietary restrictions", "other"],
    ).ask()

    pass


# TODO: implement
def create_issue_action(user: User):
    pass


# TODO: implement
def chat_with_customer_service_action(user: User):
    pass
