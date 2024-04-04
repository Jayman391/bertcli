from src.drivers._driver import Driver
from util._session import Session
import sys

class GlobalDriver(Driver):
    """
    The GlobalDriver class is a subclass of the Driver class and represents a global driver for topic modeling.

    Attributes:
        session (Session): The session object associated with the driver.

    Methods:
        __init__(self, session=None): Initializes a new instance of the GlobalDriver class.
        _run_topic_model(self, from_file=False): Runs the topic modeling process.
        _fit_model(self, model): Fits the topic model to the session data and extracts the topics.
        _process_topic_choice(self, model, value, topics): Processes the topic choice and saves the results.
        _write_logs(self, directory): Writes the logs to a JSON file.
    """

    def __init__(self, session: Session = None):
        """
        Initializes a new instance of the GlobalDriver class.

        Args:
            session (Session, optional): The session object associated with the driver. Defaults to None.
        """
        if sys.platform.startswith("linux"):
            self.file = ""
        else:
            self.file = "file://"
        super().__init__(session)

   