from bertcli.menus._menu import Menu

class Topic(Menu):
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
            "Saving"
        ]

        super().__init__(options, is_leaf, is_root)