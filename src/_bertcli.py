from src.loading._dataloader import DataLoader

class BERTCLI:

    def __init__(self, global_data_path: str = None, global_config_path: str = None, global_optmization_path: str = None):    

        print("\nWelcome to the BERTopic CLI!")

        self.global_session = None

        loader = DataLoader()

        self.global_session = loader.initialize_session(
            global_data_path, global_config_path, global_optmization_path
        )
