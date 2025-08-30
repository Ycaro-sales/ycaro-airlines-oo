from questionary import Choice
import questionary
from typing import Tuple, Any, Callable
from rich.console import Console

console = Console()


def menu_factory(title: str, options: list[Tuple[str, Callable]]):
    choices: list[Choice] = [Choice(c[0], c[1]) for c in options]
    choices.append(Choice("Go Back", value=""))

    def menu() -> Any:
        while True:
            selection = questionary.select(title, choices=choices).ask()
            match selection:
                case "":
                    break
                case None:
                    break
                case _:
                    selection()

    return menu
