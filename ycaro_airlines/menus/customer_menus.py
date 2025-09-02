# from ycaro_airlines.menus import menu_factory, console
from ycaro_airlines.actions.booking_actions import (
    BookFlightAction,
)

from ycaro_airlines.actions.flight_actions import (
    SearchFlightAction,
)
from ycaro_airlines.menus.menu import Menu, UIComponent
from ycaro_airlines.models import Customer
from ycaro_airlines.models.user import User

# TODO: Change Customer to user and check


class CustomerMenu(Menu):
    title: str = "Customer Menu"

    def __init__(self, user: User, parent) -> None:
        self.children: list[UIComponent] = [
            FlightsMenu(user, self),
            # BookingsMenu(self),
            # IssuesMenu(self),
        ]
        super().__init__(user, parent)


# def customer_service_menu(user: Customer):
#     options: list[Tuple[str, Callable]] = [
#         ("See issues", partial(issues_menu, user=user)),
#         ("Create issue", partial(create_issue_action, user=user)),
#     ]
#     menu_factory("Customer Service", options)()


# TODO: implement
def issues_menu(user: Customer):
    # questionary.select("Select one of the following issues:", choices=)
    pass


# def bookings_menu(user: Customer):
#     Booking.print_bookings_table(user.id, console)
#
#     if len(Booking.list_bookings(user.id)) == 0:
#         print("There are no bookings to manage!")
#         return
#
#     booking_id = questionary.autocomplete(
#         "Type the id of the booking you wish to manage:(type 'q' to go back)",
#         choices=[str(i.id) for i in Booking.list_bookings(user.id)],
#         validate=lambda x: (
#             True
#             if x in {str(i.id) for i in Booking.list_bookings(user.id)} or x == "q"
#             else False
#         ),
#     ).ask()
#
#     if booking_id == "q" or not booking_id:
#         return
#
#     booking = Booking.bookings[int(booking_id)]
#     booking.print_booking_table(console)
#
#     options: list[Tuple[str, Callable]] = [
#         (
#             "Cancel Booking",
#             partial(cancel_booking_action, user=user, booking=booking),
#         ),
#         ("Change Seat", partial(select_seat_action, booking=booking)),
#         ("Online Check-in", partial(check_in_action, user=user, booking=booking)),
#     ]
#
#     if booking.status != BookingStatus.booked:
#         options = [
#             (
#                 "Ver passagem",
#                 partial(booking.print_booking_table, console=console),
#             )
#         ]
#
#     menu_factory("Booking management", options)()


class FlightsMenu(Menu):
    title: str = "Search Flights Menu"

    def __init__(self, user: User, parent: "UIComponent | None" = None):
        self.children: list[UIComponent] = [
            BookFlightAction(user, self),
            SearchFlightAction(user, self),
        ]
        super().__init__(user=user, children=self.children, parent=parent)


# def flights_menu(user: Customer):
#     options: list[Tuple[str, Callable]] = [
#         ("Book flight", partial(book_flight_action, user=user)),
#         ("Search flights", search_flight_action),
#     ]
#
#     Flight.print_flights_table(console)
#
#     menu_factory("Flights", options)()
