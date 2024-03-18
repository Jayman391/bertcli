import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.bertcli.menus._menu import Menu

class OptimizationMenu(Menu):
  def __init__(self):
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

    super().__init__(options, is_leaf, is_root)