import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.bertcli.menus._menu import Menu

class FineTuneMenu(Menu):
    def __init__(self):
        is_root = False
        is_leaf = True
        options = [
            "Enable 2-grams",
            "Enable 3-grams",
            "Ignore Words",
            "Enable BM25 weighting",
            "Reduce frequent words",
            "Enable KeyBERT algorithm",
            "Enable ZeroShotClassification",
            "Enable Maximal Marginal Relevance",
            "Enable Part of Speech filtering",
        ]

        super().__init__(options, is_leaf, is_root)