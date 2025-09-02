from itertools import chain
from typing import Callable, Tuple

import questionary
from ycaro_airlines.menus.customer_menus import CustomerMenu
from ycaro_airlines.menus.menu import Action, Menu, UIComponent
from ycaro_airlines.models.customer import Customer
from ycaro_airlines.models.customer_service import CustomerServiceWorker
from ycaro_airlines.models.user import User


class LoginAction(Action):
    title: str = "Login"

    def operation(self):
        username = questionary.select(
            "Select a user to login:", choices=[v.username for v in User.list()]
        ).ask()

        if username is None:
            return

        user = User.get_by_username(username)

        if user is None:
            print("Invalid Username!")
            return

        if isinstance(user, Customer):
            return CustomerMenu(user)
        elif isinstance(user, CustomerServiceWorker):
            return WorkerMenu(user)

        return None


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


class SignupAction(Action):
    title: str = "Sign Up"

    def operation(self, user: None = None):
        role = questionary.select(
            "What type of user do you want to register?",
            choices=["Customer", "Customer Service Worker"],
        ).ask()
        username = questionary.text(
            "Username:",
            default="",
            validate=lambda x: (
                True if x not in {v.username for v in Customer.list()} else False
            ),
        ).ask()

        if role == "Customer":
            Customer(username=username)
        elif role == "Customer Service Worker":
            CustomerServiceWorker(username=username)
        else:
            raise ValueError("User must have a role")

        print("Sign Up Successful!")

        return self.parent


class AccountsMenu(Menu):
    title: str = "Accounts Menu"

    def __init__(self, parent: "UIComponent | None" = None):
        self.children: list[UIComponent] = [SignupAction(self)]
        super().__init__(children=self.children, title=self.title, parent=parent)


def accounts_menu():
    options: list[Tuple[str, Callable]] = [
        ("Login", login_action),
        ("Sign up", signup_action),
    ]

    menu_factory("Accounts Menu", options=options)()
