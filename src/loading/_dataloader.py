import json
import pandas as pd
from src.util._session import Session

class DataLoader:

    def __init__(self):
        pass

    def _load_data(self, data_path: str):
        """
        Load data from a file.

        Args:
        data_path (str): Path to the data file.

        Returns:
        data: Loaded data.
        """

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

        return data


    def _load_config(self, config_path: str):
        """
        Load configuration from a file.

        Args:
        config_path (str): Path to the configuration file.

        Returns:
        config: Loaded configuration.
        """

        flag = True

        if config_path.endswith(".json"):
            with open(config_path, "r") as file:
                config = json.load(file)

            flag = False

        if flag:
            raise Exception("File type not supported")

        return config


    def _no_args_passed(self):
        """
        Handle case when no arguments are passed.

        Args:
        None

        Returns:
        data: Loaded data.
        config: Loaded configuration.
        """

        data = []

        data_bool = input("Would you like to use a dataset for this session? (y/n): ")

        if data_bool.lower() == "y":
            data_path = input("Please enter the path to the data file: ")

            data = self._load_data(data_path)

        config = {}

        config_bool = input("Do you want to load topic model configurations? (y/n): ")

        if config_bool.lower() == "y":
            config_path = input("Please enter the path to the configuration file:")

            config = self._load_config(config_path)

        return data, config

    def initialize_session(self, data_path: str = None, config_path: str = None, optimization_path: str = None):
        
        data = []
        config = {}
        opt = {}

        if data_path is None and config_path is None:
            data, config = self._no_args_passed()

        if data_path is not None:
            data = self._load_data(data_path)
            print(f"Loaded data from {data_path}")

        if config_path is not None:
            config = self._load_config(config_path)
            print(f"Loaded config from {config_path}")

        if optimization_path is not None:
            opt = self._load_config(optimization_path)
            print(f"Loaded optimization from {optimization_path}")

        return Session(data, config, opt)
