from src.menus._menu import Menu
from util._session import Session


class TopicPlottingMenu(Menu):
    def __init__(self, session: Session, parent: Menu = None):
        is_root = False
        is_leaf = True
        options = [
            "Enable Topic Visualizations",
            "Enable Document Visualizations",
            "Enable Term Visualizations",
            "Enable All Visualizations",
            "Specify Plot Directory",
            "Specify Web Browser",
        ]

        self.name = "Plotting"

        super().__init__(session, options, is_leaf, is_root, name=self.name)

    def handle_choice(self, choice: int):
        if choice == 5:
            dir = self.prompt_string("Enter the plot directory: ")
            print(f"directory : {dir}")
            return dir
        elif choice == 6:
            browsers = ["firefox", "chrome", "safari", "opera"]
            for i, browser in enumerate(browsers):
                print(f"{i + 1}. {browser}")
            choice = self.prompt_numeric("Choose a browser: ")
            return browsers[choice - 1]
        else:
            return self.options[choice - 1]
