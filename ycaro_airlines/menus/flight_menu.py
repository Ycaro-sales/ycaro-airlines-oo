from ycaro_airlines.menus.actions.booking.book_flight_action import BookFlightAction
from ycaro_airlines.menus.actions.flight_actions import SearchFlightAction
from ycaro_airlines.menus.menu import Menu, UIComponent
from ycaro_airlines.models.user import User


class FlightsMenu(Menu):
    title: str = "Search Flights Menu"

    def __init__(self, user: User, parent: "UIComponent | None" = None):
        self.children: list[UIComponent] = [
            BookFlightAction(user, self),
            SearchFlightAction(user, self),
        ]
        super().__init__(user=user, children=self.children, parent=parent)
