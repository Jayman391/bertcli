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
            "Enable Zero Shot Classification",
            "Enable Maximal Marginal Relevance",
            "Enable Part of Speech filtering",
        ]

        self.name = "Fine Tuning"

        super().__init__(session, options, is_leaf, is_root, name=self.name)

    def handle_choice(self, choice: int):
        if choice == len(self.options):
            self.exit()
        else:
            if choice == 3 or choice == 7:
                prompt = True
                words = ["Ignore Words"] if choice == 3 else ["Zero Shot"]
                while prompt:
                    word = input("Input a word, or leave blank to continue: ")
                    if word != "":
                        words.append(word.lower())
                    else:
                        return words
            else:
                return self.options[choice - 1]
