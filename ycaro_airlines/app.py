from ycaro_airlines.menus.menu import UIComponent

import os
from ycaro_airlines.models.user import User


def clear_screen():
    os.system("clear")


class App:
    def __init__(self, first_screen: UIComponent) -> None:
        self.current_screen = first_screen
        self.logged_user: User | None = None

    def run(self):
        while True:
            # clear_screen()
            if (next_screen := self.current_screen.operation()) is None:
                break

            self.current_screen = next_screen
