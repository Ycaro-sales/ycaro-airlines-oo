from ycaro_airlines.menus.account_menus import accounts_menu
from ycaro_airlines.models import Flight, Customer


def main():
    for _ in range(0, 20):
        Flight.mock_flight()

    Customer("Default")

    accounts_menu()


if __name__ == "__main__":
    main()
