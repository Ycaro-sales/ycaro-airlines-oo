from ycaro_airlines.menus.account_menus import AccountsMenu
from ycaro_airlines.app import App


def main():
    myapp = App(AccountsMenu())
    myapp.run()


if __name__ == "__main__":
    main()
