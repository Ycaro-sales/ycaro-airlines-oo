from itertools import chain
from typing import Callable, Tuple

import questionary
from ycaro_airlines.menus import menu_factory, customer_menu
from ycaro_airlines.models.customer import Customer


def login_action():
    username = questionary.select(
        "Select a user to login:",
        choices=[v.username for v in chain(Customer.customers.values())],
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
        validate=lambda x: True
        if x not in {v.username for v in Customer.customers.values()}
        else False,
    ).ask()
    Customer(username=username)
    print("Sign Up Successful!")


def accounts_menu():
    options: list[Tuple[str, Callable]] = [
        ("Login", login_action),
        ("Sign up", signup_action),
    ]

    menu_factory("Accounts Menu", options=options)()
