from src.menus._menu import Menu

class GridSearchMenu(Menu):
  def __init__(self):
    is_root = False
    is_leaf = True
    options = [
      'Enable Successive Halving',
      'Enable Random Search',
      'Greedy',
      'Random Walk',
      'Genetic Algorithm',
    ]

    super().__init__(options, is_leaf, is_root)