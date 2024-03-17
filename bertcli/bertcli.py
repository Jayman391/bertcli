import argparse
from bertcli.loading._dataloader import initialize_session


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

        self.global_session = initialize_session(
            global_data_path, global_config_path, global_optmization_path
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BERTopic CLI")

    parser.add_argument(
        "--data", type=str, required=False, help="Path to the global data file"
    )
    parser.add_argument(
        "--config", type=str, required=False, help="Path to the global config file"
    )

    args = parser.parse_args()

    cli = BERTCLI(data_path=args.data, config_path=args.config)
