from src.menus._menu import Menu
from util._session import Session

class TopicPlottingMenu(Menu):
    def __init__(self, session:Session, parent: Menu = None):
        is_root = False
        is_leaf = True
        options = [
            "Visualize Topics",
            "Visualize Documents",
            "Visualize Document Hierarchy",
            "Visualize Topic Hierarchy",
            "Visualize Topic Tree",
            "Visualize Topic Terms",
            "Visualize Topic Similarity",
            "Visualize Term Score Decline",
            "Visualize Topic Probability Distribution",
            "Visualize Topics over Time",
            "Visualize Topics per Class",
        ]

        self.name = "Plotting"

        super().__init__(session, options, is_leaf, is_root, name=self.name)

