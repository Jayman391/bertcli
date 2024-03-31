import json
import pandas as pd
from src.util._session import Session
from random import shuffle

class DataLoader:
    def __init__(self):
        pass

    def prompt_yes_no(self, message: str):
        response = input(message).lower()
        if not response in ["y", "n"]:
            print("Invalid response")
            return self.prompt_yes_no(message)
        return response

    def prompt_load_data(self, num_samples: int = 0):
        data_bool = self.prompt_yes_no(
            "Would you like to use a dataset for this session? (y/n): "
        )

        data = []

        if data_bool.lower() == "y":
            data_path = input("Please enter the path to the data file: ")

            if num_samples > 0:
                data = self._load_data(data_path, num_samples)
            else:
                data = self._load_data(data_path)

            sample_bool = self.prompt_yes_no(
                "Would you like to sample the data? (y/n): "
            )

            if sample_bool.lower() == "y":
                sample_size = 10000

                try:
                    sample_size = int(input("Please enter the sample size: "))
                except ValueError:
                    print("Invalid input. Defaulting to 10000")

                shuffle(data)
                data = data[:sample_size]
                

        return data

    def prompt_load_tm_config(self):
        config_bool = self.prompt_yes_no(
            "Do you want to load topic model configurations? (y/n): "
        )

        config = {}

        if config_bool.lower() == "y":
            config_path = input("Please enter the path to the configuration file:")

            config = self._load_config(config_path)

        return config

    def prompt_load_opt_config(self):
        opt_bool = self.prompt_yes_no(
            "Do you want to load optimization configurations? (y/n): "
        )

        config = {}

        if opt_bool.lower() == "y":
            opt_path = input("Please enter the path to the optimization file:")

            config = self._load_config(opt_path)

        return config

    def initialize_session(
        self,
        data_path: str = None,
        config_path: str = None,
        optimization_path: str = None,
        num_samples: int = 0,
        save_dir: str = '',
    ):
        data = []
        config = {}
        opt = {}

        if data_path is None and config_path is None and optimization_path is None:
            data, config, opt = self._no_args_passed()

        if data_path is not None:
            data = self._load_data(data_path, num_samples)
            print(f"Loaded data from {data_path}")

        if config_path is not None:
            config = self._load_config(config_path)
            print(f"Loaded config from {config_path}")

        if optimization_path is not None:
            opt = self._load_config(optimization_path)
            print(f"Loaded optimization from {optimization_path}")

        return Session(data, config, opt, save_dir)

    def _load_data(self, data_path: str, num_samples: int = 0):
        data = None

        flag = True

        if data_path.endswith(".csv"):
            data = pd.read_csv(data_path)
            flag = False

        elif data_path.endswith(".json"):
            data = pd.read_json(data_path)
            flag = False

        if flag:
            raise Exception("File type not supported")

        if num_samples > 0:
            data = data.sample(num_samples)

        # extract the text column
        data = data["text"].to_list()

        # remove any null values and empty strings
        data = [x for x in data if str(x) != "nan" and str(x) != ""]

        return data

    def _load_config(self, config_path: str):
        flag = True

        if config_path.endswith(".json"):
            with open(config_path, "r") as file:
                config = json.load(file)

            flag = False

        if flag:
            raise Exception("File type not supported")

        return config

    def _no_args_passed(self):
        data = []
        tm_config = {}
        opt_config = {}

        if (
            self.prompt_yes_no(message="\nWould you like to configure this session? (y/n): ").lower()
            == "y"
        ):
            data = self.prompt_load_data()

            tm_config = self.prompt_load_tm_config()

            opt_config = self.prompt_load_opt_config()

        return data, tm_config, opt_config
