from abc import ABC
from util._session import Session

class Menu(ABC):
    def __init__(self, session:Session, options: list, is_leaf: bool, 
                 is_root: bool = False, parent = None):
        self._options = options
        self._is_leaf = is_leaf
        self.is_root = is_root
        self._parent: Menu = parent
        self._session: Session = session

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

    @property
    def session(self):
        return self._session
    
    @session.setter
    def session(self, session):
        if not isinstance(session, Session):
            raise TypeError("session must be a Session object")
        self._session = session

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
        try:
            return int(choice)
        except ValueError:
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
        elif choice == len(self.options) - 1:
            return self.back()
        else:
            if self.is_leaf:
                return self.options[choice - 1]
            else:
                return self.menus[self.options[choice - 1]]

    def _map_options_to_menus(self, options: list, menus: list):
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
