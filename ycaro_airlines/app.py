from ycaro_airlines.menus.menu import UIComponent


class App:
    def __init__(self, first_screen: UIComponent) -> None:
        self.current_screen = first_screen

    def run(self):
        while True:
            if (next_screen := self.current_screen.operation()) is None:
                break

            self.current_screen = next_screen
