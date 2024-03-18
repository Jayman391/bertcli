from src.menus._menu import Menu

class OptimizationPlottingMenu(Menu):
  def __init__(self):
    is_root = False
    is_leaf = True
    options = [
     "Plot Convergence",
     "Plot Evaluations",
     "Plot Objective"
    ]

    super().__init__(options, is_leaf, is_root)