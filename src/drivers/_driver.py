from abc import ABC
from src.menus._menu import Menu
from src.loading._dataloader import DataLoader
from util._session import Session
import os
import json


class Driver(ABC):
    """
    Abstract base class for drivers.
    """

    def __init__(self, session: Session = None):
        self._session: Session = session
        self._session_data = {}

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session):
        self._session = session

    @property
    def session_data(self):
        return self._session_data

    @session_data.setter
    def session_data(self, key, value):
        self._session_data[key] = value

    def initialize_session(
        self,
        data_path: str = None,
        config_path: str = None,
        ft_config_path: str = None,
        num_samples: int = 0,
        save_dir: str = '',
    ):
        """
        Initializes the session with the given parameters.

        Args:
            data_path (str): Path to the data.
            config_path (str): Path to the configuration file.
            num_samples (int): Number of samples.
            save_dir (str): Directory to save the session.

        Returns:
            Session: The initialized session.
        """
        loader = DataLoader()
        self.session = loader.initialize_session(
            data_path, config_path, ft_config_path, num_samples, save_dir
        )

        return self.session

    def log(self, type: str, message: str):
        """
        Logs a message of the given type.

        Args:
            type (str): The type of the log message.
            message (str): The log message.

        Returns:
            dict: A dictionary containing the logged message.
        """
        if type not in self.session.logs.keys():
            self.session.logs[type] = []

        self.session.logs[type].append(message)

        return {type: message}

    def _run_menu(self, menu: Menu):
        """
        Runs the given menu.

        Args:
            menu (Menu): The menu to run.

        Returns:
            Any: The response from the menu.
        """
        menu.display()
        choice = menu.prompt_numeric("Choose an option: ")
        if choice < 1 or choice > len(menu.options):
            print("Invalid choice. Please choose a valid number.")
            choice = menu.prompt_numeric("Choose an option: ")
        response = menu.handle_choice(choice)

        return response

    def _process_response(self, response):
        """
        Processes the given response.

        Args:
            response (Any): The response to process.

        Returns:
            Any: The processed response.
        """
        if isinstance(response, Menu):
            return self._run_menu(response)
        else:
            return response
    
    def _write_logs(self, directory):
        """
        Writes the logs to a JSON file.

        Args:
            directory (str): The directory where the logs should be saved.
        """
        errors = self.session.get_logs("errors")
        data = self.session.get_logs("data")
        logs = {"errors": errors, "data": data}
        if directory != "" and directory is not None:
            if not os.path.isdir(directory):
                os.makedirs(directory)
            with open(f"{directory}/logs.json", "w") as f:
                json.dump(logs, f)
        else:
            with open(f"logs.json", "w") as f:
                json.dump(logs, f)
