from src.menus._menu import Menu
from util._session import Session
from menus.topic._embeddings import EmbeddingsMenu
from menus.topic._dim_red import DimensionalityReductionMenu
from menus.topic._cluster import ClusterMenu
from menus.topic._fine_tune import FineTuneMenu
from menus.topic._plotting import TopicPlottingMenu
from menus._configmenu import ConfigMenu
from random import shuffle


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
            "Set Sample Size",
            "Load Topic Model Configuration",
            "Save Session Data",
            "Run Topic Model",
        ]

        menus = [
            EmbeddingsMenu(session),
            DimensionalityReductionMenu(session),
            ClusterMenu(session),
            FineTuneMenu(session),
            TopicPlottingMenu(session),
            None,
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

                sample_size = self.prompt_numeric("Please enter the sample size: ")

                data = self.session.data

                shuffle(data)
                self.session.data = data[:sample_size]

                return self
            elif choice == 7:
                load_file = input(
                    "Please enter the path of the json file to load the configuration: "
                )
                self.session.logs["data"].append({"Topic": "load_file " + load_file})
                return self
            elif choice == 8:
                save_dir = input(
                    "Please enter the path of the directory to save this sessions data: "
                )
                self.session.logs["data"].append({"Topic": "save_dir " + save_dir})
                return self
            elif choice == 9:
                return self.session.build_topic_model()
            else:
                return self.menus[self.options[choice - 1]]
