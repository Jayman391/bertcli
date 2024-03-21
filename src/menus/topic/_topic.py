from src.menus._menu import Menu
from util._session import Session
from menus.topic._embeddings import EmbeddingsMenu
from menus.topic._dim_red import DimensionalityReductionMenu
from menus.topic._cluster import ClusterMenu
from menus.topic._fine_tune import FineTuneMenu
from menus.topic._plotting import TopicPlottingMenu
from menus._configmenu import ConfigMenu


class TopicMenu(Menu):
    def __init__(self, session: Session):
        is_root = False
        is_leaf = False
        options = [
            "Select LLM to generate Embeddings",
            "Select Dimensionality Reduction Technique",
            "Select Clustering Technique",
            "Fine Tuning",
            "Plotting",
            "Save Session Configuration",
            "Run Topic Model",
            "Load Session Configuration",
        ]

        menus = [
            EmbeddingsMenu(session),
            DimensionalityReductionMenu(session),
            ClusterMenu(session),
            FineTuneMenu(session),
            TopicPlottingMenu(session),
            None,
            None,
            ConfigMenu(session),
        ]

        self.name = "Topic"

        super().__init__(session, options, is_leaf, is_root, name=self.name)

        self.map_options_to_menus(options, menus)

    def handle_choice(self, choice: int):
        if choice == len(self.options):
            self.exit()
        else:
            if choice == len(self.options) - 1:
                self.session.logs["info"].append(f"User went back to {self.parent}")
                return self.back()
            elif choice == 6:
                self.session.logs["data"].append(
                    {
                        "save_file": input(
                            "Please enter the path of the json file to save the configuration: "
                        )
                    }
                )
                return self
            elif choice == 7:
                self.session.logs["data"].append({"Topic": "run_topic_model"})
                return self
            elif choice == 8:
                self.session.logs["data"].append(
                    {
                        "load_file": input(
                            "Please enter the path of the json file to load the configuration: "
                        )
                    }
                )
                return self
            else:
                return self.menus[self.options[choice - 1]]
