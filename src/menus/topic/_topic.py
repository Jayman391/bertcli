from src.menus._menu import Menu
from util._session import Session

class TopicMenu(Menu):
    def __init__(self, session: Session):
        is_root = False
        is_leaf = False
        options = [
            "Load Data",
            "Load Configuration",
            "Select LLM to generate Embeddings",
            "Select Dimensionality Reduction Technique",
            "Select Clustering Technique",
            "Fine Tuning",
            "Plotting",
            "Saving",
            "Run Topic Model",
        ]

        super().__init__(session, options, is_leaf, is_root)
