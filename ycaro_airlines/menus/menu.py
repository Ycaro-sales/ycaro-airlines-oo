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


class Menu(UIComponent, ABC):
    def __init_subclass__(cls) -> None:
        cls.menu_options: list[UIComponent] = []
        return super().__init_subclass__()

    def __init__(self, title: str, parent: UIComponent | None):
        super().__init__(title, parent)

    def operation(self, user: None = None) -> UIComponent | None:
        choices: list[questionary.Choice] = [
            questionary.Choice(option.title, option) for option in self.menu_options
        ]

        choices.append(questionary.Choice("Go Back", value=self.parent))

        selection = questionary.select(self.title, choices=choices).ask()

        return selection

    def add(self, menu_options: UIComponent):
        self.menu_options.append(menu_options)
        menu_options.parent = self


class Action(UIComponent, ABC):
    @abstractmethod
    def operation(self, user: None = None) -> UIComponent | None:
        pass
