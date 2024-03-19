from src.loading._dataloader import DataLoader
from src.drivers._global_driver import GlobalDriver
from src.menus._landing import Landing

class NLLPCLI:
    def __init__(
        self,
        global_data_path: str = None,
        global_config_path: str = None,
        global_optmization_path: str = None,
    ):
        print("\nWelcome to the BERTopic CLI!")

        self.driver = GlobalDriver()

        self.global_session = self.driver.initialize_session(
            data_path=global_data_path,
            config_path=global_config_path,
            optimization_path=global_optmization_path,
        )
        self.driver.log("info", "Initialized Global Session Object and Global Driver")

        self.landing = Landing(session=self.driver.session)
        self.driver.log("info", "Initialized Landing Menu")

    def run(self):
        pass

