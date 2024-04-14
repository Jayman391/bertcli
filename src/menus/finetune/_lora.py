from src.menus._menu import Menu
from util._session import Session

class LORAMenu(Menu):
    def __init__(self):
        is_root = False
        is_leaf = True
        options = [
            "set r value",
            "set alpha",
        ]

        menus = [
            None,
            None,
          ]

        self.name = "Fine Tune"

        super().__init__(options, is_leaf, is_root)

        self.map_options_to_menus(options, menus)

    def handle_choice(self, choice: int):
        if choice == len(self.options):
            self.exit()
        if choice == len(self.options) - 1:
            return self.back()
        if choice == 1:
            r = self.prompt_numeric("Please enter the r value:")
            self.session.log("data", {"Fine Tune" : f"r {r}"})
            return self
        if choice == 2:
            alpha = self.prompt_numeric("Please enter the alpha value:")
            self.session.log("data", {"Fine Tune" : f"alpha {alpha}"})
            return self