from abc import ABC, abstractmethod
import questionary


# TODO: implement composite pattern
class UIComponent(ABC):
    def __init__(self, title: str, parent: "UIComponent | None"):
        self._parent: UIComponent | None = parent
        self.title = title

    @abstractmethod
    def operation(self, user: None = None) -> "UIComponent | None":
        pass

    @property
    def parent(self) -> "UIComponent | None":
        return self._parent

    @parent.setter
    def parent(self, value: "UIComponent"):
        self._parent = value


class Menu(UIComponent):
    def __init__(
        self, title: str, options: list[UIComponent], parent: UIComponent | None
    ):
        super().__init__(title, parent)
        self.title = title
        self.menu_options: list[UIComponent] = options

    def operation(self, user: None = None) -> UIComponent | None:
        choices: list[questionary.Choice] = [
            questionary.Choice(o.title, o) for o in self.menu_options
        ]

        choices.append(questionary.Choice("Go Back", value=self.parent))

        selection = questionary.select(self.title, choices=choices).ask()

        return selection

    def add(self, menu_options: UIComponent):
        self.menu_options.append(menu_options)
        menu_options.parent = self


class Action(UIComponent):
    def operation(self, user: None = None) -> UIComponent | None:
        return self.parent
