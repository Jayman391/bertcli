from src.menus._menu import Menu


class ClusterMenu(Menu):
    def __init__(self):
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

        super().__init__(options, is_leaf, is_root)
