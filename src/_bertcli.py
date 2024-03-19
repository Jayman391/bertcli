from src.loading._dataloader import DataLoader
from src.drivers._global_driver import GlobalDriver
from src.menus._landing import Landing

class BERTCLI:
    def __init__(
        self,
        global_data_path: str = None,
        global_config_path: str = None,
        global_optmization_path: str = None,
    ):
        print("\nWelcome to the BERTopic CLI!")

        driver = GlobalDriver()

        self.global_session = driver.initialize_session(
            data_path=global_data_path,
            config_path=global_config_path,
            optimization_path=global_optmization_path,
        )

    def run(self):
        pass
