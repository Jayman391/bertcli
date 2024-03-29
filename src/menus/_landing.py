from src.menus._menu import Menu
from src.menus.topic._topic import TopicMenu
from src.menus._configmenu import ConfigMenu
from util._session import Session
from src.loading._dataloader import DataLoader


class Landing(Menu):
    def __init__(self, session: Session):
        is_root = True
        is_leaf = False
        options = [
            "Run a Topic Model",
            "Run a Classification Model",
            "Run an Optimization routine",
            "Load Global Configuration Files",
        ]

        self.dataloader = DataLoader()

        self.name = "Landing"

        super().__init__(session, options, is_leaf, is_root, name=self.name)

        menus = [
            TopicMenu(session),
            None,
            None,
            ConfigMenu(session),
        ]

        self.map_options_to_menus(options, menus)
