from abc import ABC
from src.menus._menu import Menu
from src.loading._dataloader import DataLoader
from util._session import Session


class Driver(ABC):
    def __init__(self):
        self._session:Session = None
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
        optimization_path: str = None,
    ):
        loader = DataLoader()
        self.session = loader.initialize_session(
            data_path, config_path, optimization_path
        )

        return self.session

    def log(self, type: str, message: str):
        if type not in self.session.logs.keys():
            self.session.logs[type] = []

        self.session.logs[type].append(message)

        return {type:message}

    def run_menu(self, menu : Menu):
        menu.display()
        choice = menu.prompt_numeric("Choose an option: ")
        response = menu.handle_choice(choice)

        return response

    def run_model(self):
        pass
