from src.menus._menu import Menu
from util._session import Session

class OptimizationMenu(Menu):
    def __init__(self, session: Session):
        is_root = False
        is_leaf = False
        options = [
            "Choose a section to optimize",
            "Choose a scoring function",
            "Enable Bayesian Optimization",
            "Choose a heuristic for optimization",
            "Configure Hyperparameter Distributions",
            "Configure Plotting",
            "Run Optimization",
        ]

        super().__init__(session, options, is_leaf, is_root)
