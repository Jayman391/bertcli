from src.menus._menu import Menu


class DimensionalityReductionMenu(Menu):
    def __init__(self):
        is_root = False
        is_leaf = True
        options = [
            "UMAP",
            "PCA",
            "t-SNE",
            "Truncated SVD",
            "Factor Analysis",
        ]

        super().__init__(options, is_leaf, is_root)
