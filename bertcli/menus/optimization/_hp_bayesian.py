from bertcli.menus._menu import Menu

class BayesianHyperParameterMenu(Menu):
  def __init__(self):
    is_root = False
    is_leaf = True
    options = [
      "Choose a section to optimize",
      "Choose a scoring function",
      "Enable Bayesian Optimization",
      "Choose a heuristic for optimization",
      "Configure Hyperparameter Distributions",
      "Configure Plotting",
      "Run Optimization",
    ]

    super().__init__(options, is_leaf, is_root)