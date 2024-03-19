from src.menus._menu import Menu
from util._session import Session

class ClusterMenu(Menu):
    def __init__(self, session:Session):
        is_root = False
        is_leaf = True
        options = [
            "hdbscan",
            "kmeans",
            "spectral clustering",
            "dbscan",
            "agglomerative clustering",
            "birch",
            "affinity propagation",
            "mean shift",
        ]

        super().__init__(session, options, is_leaf, is_root)
