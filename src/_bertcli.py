from src.loading._dataloader import DataLoader

class BERTCLI:
    """
    Command Line Interface for BERTopic.

    Args:
      global_data_path (str): Path to the data file.
      global_config_path (str): Path to the configuration file.

    Raises:
      Exception: If data_path is None and config_path is not None.

    Attributes:
      None

    """

    def __init__(self, global_data_path: str = None, global_config_path: str = None, global_optmization_path: str = None):
        """
        Initialize the CLI class.

        Args:
          global_data_path (str): Path to the data file.
          global_config_path (str): Path to the configuration file.

        Returns:
          None
        """

        print("\nWelcome to the BERTopic CLI!")

        self.global_session = DataLoader().initialize_session(
            global_data_path, global_config_path, global_optmization_path
        )
