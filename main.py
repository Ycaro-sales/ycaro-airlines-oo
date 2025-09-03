from ycaro_airlines.menus.account_menus import AccountsMenu, accounts_menu
from ycaro_airlines.models import Flight, Customer
from ycaro_airlines.app import App


def main():
    for _ in range(5):
        Flight.mock_flight()
    myapp = App(AccountsMenu())
    myapp.run()


if __name__ == "__main__":
    main()
