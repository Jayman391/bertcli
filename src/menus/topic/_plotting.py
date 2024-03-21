from src.menus._menu import Menu
from util._session import Session

class TopicPlottingMenu(Menu):
    def __init__(self, session:Session, parent: Menu = None):
        is_root = False
        is_leaf = True
        options = [
            "Enable Topic Visualizations",
            "Enable Document Visualizations",
            "Enable Term Visualizations",
            "Enable All Visualizations",
        ]

        self.name = "Plotting"

        super().__init__(session, options, is_leaf, is_root, name=self.name)

