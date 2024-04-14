from src.menus._menu import Menu
from util._session import Session

class TrainValMenu(Menu):
    def __init__(self, session: Session):
        is_root = False
        is_leaf = False
 
        options = [
            "Specify Learning Rate",
            "Specify Number of Epochs",
            "Specify Train Test Split Ratio",
        ]

        menus = [
            None,
            None,
            None,
        ]

        self.name = "Train"

        super().__init__(session, options, is_leaf, is_root)

        self.map_options_to_menus(options, menus)

    def handle_choice(self, choice: int):
        if choice == len(self.options):
            self.exit()
        if choice == len(self.options) - 1:
            return self.back()
        if choice == 1:
            lr = self.prompt_string("Please enter the learning rate:")
            self.session.log("data", {"Train" : f"learning rate {lr}"})
            return self
        if choice == 2:
            epochs = self.prompt_string("Please enter the number of epochs:")
            self.session.log("data", {"Train" : f"epochs {epochs}"})
            return self
        if choice == 3:
            split = self.prompt_numeric("Please enter the train test split ratio:")
            while split < 0 or split > 1:
                split = self.prompt_numeric("Please enter a valid train test split ratio between 0 and 1:")
            self.session.log("data", {"Train" : f"train-test-split-ratio {split}"})
            return self
     

