import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.bertcli.menus._menu import Menu

class Landing(Menu):
    def __init__(self):
        is_root = True
        is_leaf = False
        options = [
            "Run a Topic Model",
            "Run multiple Topic Models",
            "Load Global Data",
            "Load Global Topic Model Configuration",
            "Run an Optimization routine for a Topic Model (GPU reccomended)",
            "Run an Optimization routine for multiple Topic Models (GPU reccomended)",
            "Load Global Optimization Configuration",
        ]

        super().__init__(options, is_leaf, is_root)
