import json
import pandas as pd
from src.util._session import Session
from random import shuffle


class DataLoader:
    """
    A class for loading and processing data for a session.

    Methods:
    - prompt_yes_no: Prompt the user for a yes/no response.
    - prompt_load_data: Prompt the user to load a dataset for the session.
    - prompt_load_tm_config: Prompt the user to load topic model configurations.
    - prompt_ft_config: Prompt the user to load fine-tuning configurations.
    - prompt_load_opt_config: Prompt the user to load optimization configurations.
    - initialize_session: Initialize a session with data, configurations, and optimization settings.
    """

    def __init__(self):
        pass

    def prompt_yes_no(self, message: str):
        """
        Prompt the user for a yes/no response.

        Args:
        - message: The message to display to the user.

        Returns:
        - response: The user's response ('y' for yes, 'n' for no).
        """
        response = input(message).lower()
        if not response in ["y", "n"]:
            print("Invalid response")
            return self.prompt_yes_no(message)
        return response

    def prompt_load_data(self, num_samples: int = 0):
        """
        Prompt the user to load a dataset for the session.

        Args:
        - num_samples: The number of samples to load from the dataset (default: 0).

        Returns:
        - data: The loaded dataset.
        """
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
        """
        Prompt the user to load topic model configurations.

        Returns:
        - config: The loaded topic model configurations.
        """
        config_bool = self.prompt_yes_no(
            "Do you want to load topic model configurations? (y/n): "
        )

        config = {}

        if config_bool.lower() == "y":
            config_path = input("Please enter the path to the configuration file:")

            config = self._load_config(config_path)

        return config
    
    def prompt_ft_config(self):
        """
        Prompt the user to load fine-tuning configurations.

        Returns:
        - config: The loaded fine-tuning configurations.
        """
        config_bool = self.prompt_yes_no(
            "Do you want to load fine-tuning configurations? (y/n): "
        )

        config = {}

        if config_bool.lower() == "y":
            config_path = input("Please enter the path to the configuration file:")

            config = self._load_config(config_path)

        return config

    def initialize_session(
        self,
        data_path: str = None,
        config_path: str = None,
        fine_tuning_path: str = None,
        num_samples: int = 0,
        save_dir: str = "",
    ):
        """
        Initialize a session with data, configurations, and optimization settings.

        Args:
        - data_path: The path to the data file (default: None).
        - config_path: The path to the configuration file (default: None).
        - optimization_path: The path to the optimization file (default: None).
        - num_samples: The number of samples to load from the data file (default: 0).
        - save_dir: The directory to save the session (default: "").

        Returns:
        - session: The initialized session object.
        """
        data = []
        config = {}
        ft = {}

        if data_path is None and config_path is None and fine_tuning_path is None:
            data, config, ft = self._no_args_passed()

        if data_path is not None:
            data = self._load_data(data_path, num_samples)
            print(f"Loaded data from {data_path}")

        if config_path is not None:
            config = self._load_config(config_path)
            print(f"Loaded config from {config_path}")

        if fine_tuning_path is not None:
            ft = self._load_config(fine_tuning_path)
            print(f"Loaded fine-tuning from {fine_tuning_path}")

        return Session(data, config, ft, save_dir, data_path)

    def _load_data(self, data_path: str, num_samples: int = 0):
        """
        Load data from a file.

        Args:
        - data_path: The path to the data file.
        - num_samples: The number of samples to load from the data file (default: 0).

        Returns:
        - data: The loaded data.
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

        if num_samples > 0:
            data = data.sample(num_samples)

        # extract the text column
        data = data["text"].to_list()

        # remove any null values and empty strings
        data = [x for x in data if str(x) != "nan" and str(x) != ""]

        return data

    def _load_config(self, config_path: str):
        """
        Load configurations from a file.

        Args:
        - config_path: The path to the configuration file.

        Returns:
        - config: The loaded configurations.
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
        Handle the case when no arguments are passed to initialize_session.

        Returns:
        - data: The loaded data.
        - tm_config: The loaded topic model configurations.
        - opt_config: The loaded optimization configurations.
        """
        data = []
        tm_config = {}
        ft_config = {}

        if (
            self.prompt_yes_no(
                message="\nWould you like to configure this session? (y/n): "
            ).lower()
            == "y"
        ):
            data = self.prompt_load_data()

            tm_config = self.prompt_load_tm_config()

            ft_config = self.prompt_ft_config()

        return data, tm_config, ft_config
