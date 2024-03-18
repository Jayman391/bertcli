from src.menus._menu import Menu


class BayesianHyperParameterMenu(Menu):
    def __init__(self):
        is_root = False
        is_leaf = True
        options = []

        super().__init__(options, is_leaf, is_root)
