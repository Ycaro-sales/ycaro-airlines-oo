from itertools import chain
from typing import Callable, Tuple

import questionary
from ycaro_airlines.menus import menu_factory, customer_menu
from ycaro_airlines.menus.menu import Action, Menu, UIComponent
from ycaro_airlines.menus.customer_menu import CustomerMenu
from ycaro_airlines.models.customer import Customer
from ycaro_airlines.models.customer_service import CustomerServiceWorker
from ycaro_airlines.models.user import Roles, User


def login_action():
    username = questionary.select(
        "Select a user to login:",
        choices=[v.username for v in Customer.list()],
    ).ask()

    if username is None:
        return

    user = Customer.get_by_username(username)

    if user is None:
        print("Invalid Username!")
        return

    customer_menu(user)


def signup_action():
    username = questionary.text(
        "Username:",
        default="",
        validate=lambda x: (
            True if x not in {v.username for v in Customer.list()} else False
        ),
    ).ask()
    Customer(username=username)
    print("Sign Up Successful!")


def accounts_menu():
    options: list[Tuple[str, Callable]] = [
        ("Login", login_action),
        ("Sign up", signup_action),
    ]

    menu_factory("Accounts Menu", options=options)()


class LoginMenu(Menu):
    title: str = "Login"

    def operation(self) -> UIComponent | None:
        choices: list[questionary.Choice] = [
            questionary.Choice(user.username, user) for user in User.list()
        ]

        choices.append(questionary.Choice(title="Go Back", value=self.parent))

        selected_user = questionary.select(self.title, choices=choices).ask()

        if selected_user == "Go Back":
            return self.parent

        self.user = selected_user

        if self.user is None:
            print("Invalid User")
            return self.parent

        return CustomerMenu(self.user, parent=self.parent)


class SignupAction(Action):
    title: str = "Sign Up"

    def operation(self):
        username = questionary.text(
            "Username:",
            default="",
            validate=lambda x: (
                True if x not in {v.username for v in User.list()} else False
            ),
        ).ask()

        Customer(username=username)

        print("Sign Up Successful!")
        print(User.list())

        return self.parent


class AccountsMenu(Menu):
    title: str = "Accounts Menu"

    def __init__(self, user: User | None = None, parent: "UIComponent | None" = None):
        self.children: list[UIComponent] = [
            LoginMenu(user, self),
            SignupAction(user, self),
        ]
        super().__init__(user=user, children=self.children, parent=parent)
