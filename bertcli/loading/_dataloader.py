import json
import pandas as pd


def _load_data(data_path: str):
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


def _load_config(config_path: str):
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


def _no_args_passed():
    """
    Handle case when no arguments are passed.

    Args:
      None

    Returns:
      data: Loaded data.
      config: Loaded configuration.
    """

    global_data = []

    global_data_bool = input(
        "Would you like to use a global dataset for this session? (y/n): "
    )

    if global_data_bool.lower() == "y":
        data_path = input("Please enter the path to the data file: ∂")

        global_data = _load_data(data_path)

    global_config = {}

    global_config_bool = input("Do you want to load global configurations? (y/n): ")

    if global_config_bool.lower() == "y":
        config_path = input("Please enter the path to the configuration file:")

        global_config = _load_config(config_path)

    return global_data, global_config


def handle_globals(data_path: str = None, config_path: str = None):
    if data_path is None and config_path is None:
        global_data, global_config = _no_args_passed()

    if data_path is not None and config_path is None:
        global_data = _load_data(data_path)
        print(f"Loaded global data from {data_path}")
        global_config = {}

    if data_path is not None and config_path is not None:
        global_data = _load_data(data_path)
        print(f"Loaded global data from {data_path}")
        global_config = _load_config(config_path)
        print(f"Loaded global config from {config_path}")

    if data_path is None and config_path is not None:
        global_data = []

        global_config = _load_config(config_path)
        print(f"Loaded global config from {config_path}")

    return global_data, global_config
