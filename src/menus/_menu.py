from abc import ABC


class Menu(ABC):
    def __init__(self, options: list, is_leaf: bool, is_root: bool = False):
        self._options = options
        self._is_leaf = is_leaf
        self.is_root = is_root
        self._parent: Menu = None

        if not is_root:
            self.options.append("Back")

        self.options.append("Exit")

        self._menus = []

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
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if not isinstance(parent, Menu):
            raise TypeError("parent must be a Menu")
        self._parent = parent

    @property
    def menus(self):
        return self._menus

    @menus.setter
    def menus(self, option: str, menu):
        if not isinstance(menu, Menu):
            raise TypeError("must pass a Menu object")
        self._menus[option] = menu

    def display(self):
        display = []
        for i, option in enumerate(self.options):
            display.append(f"{i+1}. {option}")

        print("\n")
        for line in display:
            print(line)

        return display

    def prompt_numeric(self, prompt: str):
        choice = input(prompt)
        return self.get_choice_numeric(choice)

    def prompt_string(self, prompt: str):
        return input(prompt)

    def get_choice_numeric(self, choice):
        if not str(choice).isdigit():
            raise ValueError("Choice must be a number")

        choice = int(choice)

        if self.is_leaf:
            return self.options[choice - 1]
        else:
            return choice - 1

    def back(self):
        return self.parent

    def exit(self):
        exit()

    def handle_choice(self, choice: int):
        if choice == len(self.options):
            self.exit()
        elif choice == len(self.options) - 1:
            self.back()
        else:
            if self.is_leaf:
                return self.options[choice - 1]
            else:
                return self.menus[self.options[choice - 1]]

    def _map_options_to_menus(self, options: list, menus: list):
        if len(options[:-2]) != len(menus):
            raise ValueError("options and menus must be the same length")
        self._menus = dict(zip(options[:-2], menus))
        return self._menus
