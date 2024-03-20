from src.menus._menu import Menu
from src.menus.topic._topic import TopicMenu
from util._session import Session
from src.loading._dataloader import DataLoader

class Landing(Menu):
    def __init__(self, session:Session):
        is_root = True
        is_leaf = False
        options = [
            "Run a Topic Model",
            "Run an Optimization routine for a Topic Model (GPU reccomended)",
            "Run a Classification Model",
            "Load Global Configuration",
        ]
    
        self.dataloader = DataLoader()

        super().__init__(session, options, is_leaf, is_root)

        menus = [
            TopicMenu(session),
            None,
            None,
            None,
        ]

        self.name = "Landing"

        self._map_options_to_menus(options, menus)
        

