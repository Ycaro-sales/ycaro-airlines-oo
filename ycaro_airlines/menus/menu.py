from abc import ABC, abstractmethod
from typing import Iterable
import questionary

from ycaro_airlines.models.user import User


# TODO: implement composite pattern
class UIComponent(ABC):
    title: str = ""

    def __init_subclass__(cls, title: str = "") -> None:
        return super().__init_subclass__()

    def __init__(self, user: User | None, parent: "UIComponent | None"):
        self._parent: UIComponent | None = parent
        self.user: User | None = user

    @abstractmethod
    def operation(self) -> "UIComponent | None":
        pass

    @property
    def parent(self) -> "UIComponent | None":
        return self._parent

    @parent.setter
    def parent(self, value: "UIComponent"):
        self._parent = value


class Menu(UIComponent, ABC):
    def __init__(
        self,
        user: User | None = None,
        parent: "UIComponent | None" = None,
        children: list[UIComponent] = [],
    ):
        self.children = children
        super().__init__(user, parent)

    def operation(self) -> UIComponent | None:
        choices: list[questionary.Choice] = [
            questionary.Choice(children.title, children) for children in self.children
        ]

        choices.append(questionary.Choice(title="Go Back", value=self.parent))

        selected_child = questionary.select(self.title, choices=choices).ask()

        if selected_child == "Go Back":
            return self.parent

        return selected_child

    def add(self, children: Iterable[UIComponent]):
        for o in children:
            self.children.append(o)
            o.parent = self


class Action(UIComponent, ABC):
    @abstractmethod
    def operation(self) -> UIComponent | None:
        pass
