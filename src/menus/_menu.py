from abc import ABC
from util._session import Session
from loading._dataloader import DataLoader


class Menu(ABC):
    """
    Represents a menu in a command-line interface.

    Args:
        session (Session): The session object associated with the menu.
        options (list): The list of options available in the menu.
        is_leaf (bool): Indicates whether the menu is a leaf menu or not.
        is_root (bool, optional): Indicates whether the menu is the root menu or not. Defaults to False.
        parent (Menu, optional): The parent menu of the current menu. Defaults to None.
        name (str, optional): The name of the menu. Defaults to "Menu".

    Attributes:
        _options (list): The list of options available in the menu.
        _is_leaf (bool): Indicates whether the menu is a leaf menu or not.
        is_root (bool): Indicates whether the menu is the root menu or not.
        parent (Menu): The parent menu of the current menu.
        _menus (dict): A dictionary mapping options to child menus.
        name (str): The name of the menu.
        session (Session): The session object associated with the menu.

    Methods:
        __str__(): Returns the name of the menu.
        options(): Getter method for _options attribute.
        options(options): Setter method for _options attribute.
        is_leaf(): Getter method for _is_leaf attribute.
        is_leaf(is_leaf): Setter method for _is_leaf attribute.
        menus(): Getter method for _menus attribute.
        menus(option, menu): Setter method for _menus attribute.
        session(): Getter method for _session attribute.
        session(session): Setter method for _session attribute.
        set_parent(parent): Sets the parent menu of the current menu.
        display(): Displays the menu options.
        prompt_numeric(prompt): Prompts the user for a numeric input.
        prompt_string(prompt): Prompts the user for a string input.
        back(): Returns the parent menu.
        exit(): Exits the program.
        handle_choice(choice): Handles the user's choice and returns the appropriate action.
        map_options_to_menus(options, menus): Maps options to child menus.

    """

    def __init__(
        self,
        session: Session,
        options: list,
        is_leaf: bool,
        is_root: bool = False,
        parent=None,
        name: str = "Menu",
    ):
        self._options = options
        self._is_leaf = is_leaf
        self.is_root = is_root
        self._session: Session = session

        if not is_root:
            self.parent: Menu = parent
            self.options.append("Back")

        self.options.append("Exit")

        self._menus = []

        self.name: str = name

        self.session.logs["info"].append(f"Initialized {self.name} Menu")

    def __str__(self):
        return self.name

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, options):
        if not isinstance(options, list):
            raise TypeError("options must be a list")
        self._options = options

    @property
    def is_leaf(self):
        return self._is_leaf

    @is_leaf.setter
    def is_leaf(self, is_leaf):
        if not isinstance(is_leaf, bool):
            raise TypeError("is_leaf must be a boolean")
        self._is_leaf = is_leaf

    @property
    def menus(self):
        return self._menus

    @menus.setter
    def menus(self, option: str, menu):
        if not isinstance(menu, Menu):
            raise TypeError("must pass a Menu object")
        self._menus[option] = menu

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session: Session):
        self._session = session

    def set_parent(self, parent):
        self.parent = parent

    def display(self):
        display = []
        for i, option in enumerate(self.options):
            display.append(f"{i+1}. {option}")

        for line in display:
            print(line)

        return display

    def prompt_numeric(self, prompt: str):
        choice = input(prompt)
        flag = False
        try:
            return int(choice)
        except ValueError:
            flag = True
        if flag:
            print("Invalid choice. Please choose a number.")
            return self.prompt_numeric(prompt)

    def prompt_string(self, prompt: str):
        return input(prompt)

    def back(self):
        return self.parent

    def exit(self):
        exit()

    def handle_choice(self, choice: int):
        if choice == len(self.options):
            self.exit()
        else:
            if self.is_leaf:
                return self.options[choice - 1]
            elif self.is_root:
                return self.menus[self.options[choice - 1]]
            else:
                if choice == len(self.options) - 1:
                    return self.back()
                else:
                    return self.menus[self.options[choice - 1]]

    def map_options_to_menus(self, options: list, menus: list):
        if self.is_root:
            if len(options[:-1]) != len(menus):
                raise ValueError("options and menus must be the same length")

            self._menus = dict(zip(options[:-1], menus))
        else:
            if len(options[:-2]) != len(menus):
                raise ValueError("options and menus must be the same length")

            self._menus = dict(zip(options[:-2], menus))
            self._menus[options[-2]] = self.parent

        return self._menus
