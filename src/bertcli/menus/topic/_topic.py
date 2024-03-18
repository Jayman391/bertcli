import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.bertcli.menus._menu import Menu

class TopicMenu(Menu):
    def __init__(self):
        is_root = False
        is_leaf = False
        options = [
            "Load Data",
            "Load Configuration",
            "Select LLM to generate Embeddings",
            "Select Dimensionality Reduction Technique",
            "Select Clustering Technique",
            "Fine Tuning",
            "Plotting",
            "Saving",
            "Run Topic Model"
        ]

        super().__init__(options, is_leaf, is_root)