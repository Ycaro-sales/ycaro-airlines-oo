from ycaro_airlines.menus import menu_factory, console
from ycaro_airlines.actions.booking_actions import (
    select_seat_action,
    check_in_action,
    cancel_booking_action,
    book_flight_action,
)

from ycaro_airlines.actions.flight_actions import search_flight_action
import questionary
from ycaro_airlines.models import Customer, Booking, Flight, BookingStatus
from typing import Callable, Tuple
from functools import partial


def customer_menu(user: Customer):
    options: list[Tuple[str, Callable]] = [
        ("Browse Flights", partial(flights_menu, user=user)),
        ("My Bookings", partial(bookings_menu, user=user)),
        ("Customer Service", partial(customer_service_menu, user=user)),
    ]

    menu_factory("Customer Menu", options)()


def customer_service_menu(user: Customer):
    options: list[Tuple[str, Callable]] = [
        ("See issues and chats", partial(flights_menu, user=user)),
        ("Create issue", partial(bookings_menu, user=user)),
    ]
    menu_factory("Customer Service", options)()


def bookings_menu(user: Customer):
    Booking.print_bookings_table(user.id, console)

    if len(Booking.list_bookings(user.id)) == 0:
        print("There are no bookings to manage!")
        return

    booking_id = questionary.autocomplete(
        "Type the id of the booking you wish to manage:(type 'q' to go back)",
        choices=[str(i.id) for i in Booking.list_bookings(user.id)],
        validate=lambda x: True
        if x in {str(i.id) for i in Booking.list_bookings(user.id)} or x == "q"
        else False,
    ).ask()

    if booking_id == "q" or not booking_id:
        return

    booking = Booking.bookings[int(booking_id)]
    booking.print_booking_table(console)

    options: list[Tuple[str, Callable]] = [
        (
            "Cancel Booking",
            partial(cancel_booking_action, user=user, booking=booking),
        ),
        ("Change Seat", partial(select_seat_action, booking=booking)),
        ("Online Check-in", partial(check_in_action, user=user, booking=booking)),
    ]

    if booking.status != BookingStatus.booked:
        options = [
            (
                "Ver passagem",
                partial(booking.print_booking_table, console=console),
            )
        ]

    menu_factory("Booking management", options)()


def flights_menu(user: Customer):
    options: list[Tuple[str, Callable]] = [
        ("Book flight", partial(book_flight_action, user=user)),
        ("Search flights", search_flight_action),
    ]

    Flight.print_flights_table(console)

    menu_factory("Flights", options)()


def show_loyalty_points_action(user: Customer):
    print("not implemented!")


def claim_rewards_action(user: Customer):
    print("not implemented!")


# TODO: Implement loyalty menu
def loyalty_menu(user: Customer):
    options: list[Tuple[str, Callable]] = [
        ("Check points", partial(show_loyalty_points_action, user=user)),
        ("Claim rewards", partial(claim_rewards_action, user=user)),
    ]
    menu_factory("Flights", options)()
