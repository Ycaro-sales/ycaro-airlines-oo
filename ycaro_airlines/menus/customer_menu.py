from ycaro_airlines.menus.booking_menu import BookingMenu
from ycaro_airlines.menus.flight_menu import FlightsMenu
from ycaro_airlines.menus.menu import Menu, UIComponent
from ycaro_airlines.models.user import User


class CustomerMenu(Menu):
    title: str = "Customer Menu"

    def __init__(self, user: User, parent) -> None:
        self.children: list[UIComponent] = [
            FlightsMenu(user, self),
            BookingMenu(user, self),
        ]
        print(self.children)
        super().__init__(user, parent)
