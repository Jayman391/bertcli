from src.menus._menu import Menu
from util._session import Session
from menus.topic._embeddings import EmbeddingsMenu
from menus.topic._dim_red import DimensionalityReductionMenu
from menus.topic._cluster import ClusterMenu
from menus.topic._fine_tune import FineTuneMenu
from menus.topic._plotting import TopicPlottingMenu

class TopicMenu(Menu):
    def __init__(self, session: Session):
        is_root = False
        is_leaf = False
        options = [
            "Select LLM to generate Embeddings",
            "Select Dimensionality Reduction Technique",
            "Select Clustering Technique",
            "Fine Tuning",
            "Plotting",
            "Saving",
            "Run Topic Model",
            "Load Session Data",
            "Load Session Topic Model Configuration",
        ]
        
        menus = [
            EmbeddingsMenu(session),
            DimensionalityReductionMenu(session),
            ClusterMenu(session),
            FineTuneMenu(session),
            TopicPlottingMenu(session),
            None,
            None,
            None,
            None,
        ]

        super().__init__(session, options, is_leaf, is_root)

        self._map_options_to_menus(options, menus)
