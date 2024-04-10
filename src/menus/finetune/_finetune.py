from src.menus._menu import Menu
from util._session import Session
from menus.finetune._trainval import TrainValMenu

class FineTuneMenu(Menu):
    def __init__(self, session: Session):
        is_root = False
        is_leaf = False
        options = [
            "Upload Model Weights",
            "Upload Training Data",
            "Specify System Prompt",
            "Configure Training Parameters",
            "Commence Fine Tune",
        ]

        menus = [
            None,
            None,
            None,
            TrainValMenu(session),
            None
        ]

        self.name = "Fine Tune"

        super().__init__(session, options, is_leaf, is_root)

        self.map_options_to_menus(options, menus)

    def handle_choice(self, choice: int):
        if choice == len(self.options):
            self.exit()
        if choice == len(self.options) - 1:
            return self.back()
        if choice == 1:
            model = self.prompt("Please enter the path to the model weights:")
            self.session.log("data", {"Fine Tune" : f"weights {model}"})
        if choice == 2:
            data = self.prompt("Please enter the path to the training data:")
            self.session.log("data", {"Fine Tune" : f"data {data}"})
        if choice == 3:
            prompt = self.prompt("Please enter the system prompt: ")
            self.session.log("data", {"Fine Tune" : f"system prompt {prompt}"})
        if choice == 4:
            return self.menus[self.options[choice - 1]]
        
            
