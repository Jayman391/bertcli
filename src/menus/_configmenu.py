from src.menus._menu import Menu
from loading._dataloader import DataLoader


class ConfigMenu(Menu):
    def __init__(self, session):
        is_root = False
        is_leaf = True
        options = [
            "Input Data Path",
            "Input Topic Model Config Path",
            "Input Optimization Config Path",
        ]

        self.name = "ConfigMenu"

        super().__init__(session, options, is_leaf, is_root, name=self.name)

        self.map_options_to_menus(options, [None, None, None])

    def handle_choice(self, choice: int):
        if choice == len(self.options):
            self.exit()
        elif choice == len(self.options) - 1:
            return self.back()

        loader = DataLoader()

        if choice == 1:
            self.session.set_data(loader.prompt_load_data())

        elif choice == 2:
            self.session.set_config_topic_model(loader.prompt_load_tm_config())

        elif choice == 3:
            self.session.set_config_optimization(loader.prompt_load_opt_config())

        else:
            return self.back()
