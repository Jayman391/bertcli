from abc import ABC


class Menu(ABC):
    def __init__(self, options: list, is_leaf: bool, is_root: bool = False):
        self._options = options
        self._is_leaf = is_leaf
        self.is_root = is_root

        if not is_root:
            self.options.append("Back")
            
        self.options.append("Exit")

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

    def display(self):
        display = []
        for i, option in enumerate(self.options):
            display.append(f"{i+1}. {option}")

        print("\n")
        for line in display:
            print(line)

        return display

    def get_choice(self, choice):
        if isinstance(choice, str):
            if choice.isdigit():
                choice = int(choice)
            else:
                raise ValueError("Choice must be a number")

        if self.is_leaf:
            return self.options[choice - 1]
        else:
            return choice - 1
