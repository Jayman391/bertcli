from bertcli.menus._menu import Menu

class BayesianMenu(Menu):
  def __init__(self):
    is_root = False
    is_leaf = True
    options = [
      'Random Forest',
      'Gradient Boosting',
      'Gaussian Process',
    ]

    super().__init__(options, is_leaf, is_root)