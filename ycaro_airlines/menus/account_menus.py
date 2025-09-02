import questionary
from ycaro_airlines.menus.customer_menus import CustomerMenu
from ycaro_airlines.menus.menu import Action, Menu, UIComponent
from ycaro_airlines.models.customer import Customer
from ycaro_airlines.models.customer_service import CustomerServiceWorker
from ycaro_airlines.models.user import Roles, User


class LoginMenu(Menu):
    title: str = "Login"

    def operation(self) -> UIComponent | None:
        choices: list[questionary.Choice] = [
            questionary.Choice(user.username, user) for user in User.list()
        ]

        choices.append(questionary.Choice(title="Go Back", value=self.parent))

        selected_username = questionary.select(self.title, choices=choices).ask()

        if selected_username == "Go Back":
            return self.parent

        user = User.get_by_username(selected_username)

        if user is None:
            print("a")
            return self.parent

        if user.role == Roles.Customer:
            return CustomerMenu(user, parent=self.parent)
        if user.role == Roles.CustomerService:
            return WorkerMenu(user, parent=self.parent)

        return self.parent


class SignupAction(Action):
    title: str = "Sign Up"

    def operation(self):
        role = questionary.select(
            "What type of user do you want to register?",
            choices=["Customer", "Customer Service Worker"],
        ).ask()
        username = questionary.text(
            "Username:",
            default="",
            validate=lambda x: (
                True if x not in {v.username for v in User.list()} else False
            ),
        ).ask()
        if role == "Customer":
            Customer(username=username)
        elif role == "Customer Service Worker":
            CustomerServiceWorker(username=username)
        else:
            raise ValueError("User must have a role")

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
