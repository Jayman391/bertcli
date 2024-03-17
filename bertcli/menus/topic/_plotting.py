from bertcli.menus._menu import Menu

class Plotting(Menu):
    def __init__(self):
        is_root = False
        is_leaf = True
        options = [
            "Visualize Topics",
            "Visualize Documents",
            "Visualize Document Hierarchy",
            "Visualize Topic Hierarchy",
            "Visualize Topic Tree",
            "Visualize Topic Terms",	
            "Visualize Topic Similarity",	
            "Visualize Term Score Decline",
            "Visualize Topic Probability Distribution",	
            "Visualize Topics over Time",	
            "Visualize Topics per Class"
        ]

        super().__init__(options, is_leaf, is_root)