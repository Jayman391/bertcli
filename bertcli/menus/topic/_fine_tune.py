from bertcli.menus._menu import Menu

class FineTune(Menu):
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