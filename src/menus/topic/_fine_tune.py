from src.menus._menu import Menu
from util._session import Session


class FineTuneMenu(Menu):
    def __init__(self, session: Session, parent: Menu = None):
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

        self.name = "Fine Tuning"

        super().__init__(session, options, is_leaf, is_root, name=self.name)

    def handle_choice(self, choice: int):
        if choice == len(self.options):
            self.exit()
        else:
            if choice == 3 or choice == 5:
                prompt = True
                words = []
                while prompt:
                    prompt = input("Input a word, or leave blank to continue: ")
                    if prompt.lower() != "":
                        words.append(prompt)
                    else:
                        words.append(self.options[choice - 1])
                        return words
            else:
                return self.options[choice - 1]
