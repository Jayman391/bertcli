from src.drivers._driver import Driver
from src.drivers._global_driver import GlobalDriver
from src.drivers._tm_driver import TopicDriver
from src.drivers._tu_driver import TunerDriver
from src.menus._menu import Menu
from src.menus._landing import Landing
from src.menus.topic._topic import TopicMenu
from src.menus.optimization._optimization import OptimizationMenu
from src.obj._finetuner import FineTuner
from bertopic import BERTopic
import datetime
import traceback
from math import floor


class LNLPCLI:
    """
    The LNLPCLI class represents the command-line interface for the LNLP (Language and Natural Language Processing) system.

    Args:
        save_dir (str): The directory path to save the LNLP session data. Default is None.
        global_data_path (str): The path to the global data file. Default is None.
        global_tm_config_path (str): The path to the global configuration file. Default is None.
        global_optmization_path (str): The path to the global optimization file. Default is None.
        num_samples (int): The number of samples to use for optimization. Default is 0.
        debug (bool): Flag indicating whether to run in debug mode. Default is False.
    """

    def __init__(
        self,
        save_dir: str = None,
        global_data_path: str = None,
        global_tm_config_path: str = None,
        global_ft_config_path: str = None,
        global_optmization_path: str = None,
        num_samples: int = 0,
        debug: bool = False,
        sequence: str = '',
    ):
        self.debug = debug
        self.global_data_path = global_data_path
        self.global_tm_config_path = global_tm_config_path
        self.global_ft_config_path = global_ft_config_path
        self.global_optmization_path = global_optmization_path
        self.num_samples = num_samples
        self.save_dir = save_dir
        self.sequence = sequence

        print("\nWelcome to the LNLP CLI!")

        self.global_driver = GlobalDriver()

        self.global_session = self.global_driver.initialize_session(
            data_path=self.global_data_path,
            config_path=self.global_tm_config_path,
            ft_config_path=self.global_ft_config_path,
            optimization_path=self.global_optmization_path,
            num_samples=self.num_samples,
            save_dir=self.save_dir,
        )

        self.tm_driver = TopicDriver(session=self.global_session)
        self.tu_driver = TunerDriver(session=self.global_session)

    def run(self):
        """
        Run the LNLPCLI command-line interface.
        """
        try:
            if self.sequence != '':
                self._process_sequence(self.sequence)
            else:
                self.landing = Landing(session=self.global_driver.session)

                if self.debug:
                    self.landing.handle_choice(1)
                    return

                for _, value in self.landing.menus.items():
                    if value is not None and isinstance(value, Menu):
                        value.set_parent(self.landing)

                self._process_responses(self.landing, self.global_driver)
        except Exception as e:
            print(e)
            self.global_session.log("errors", {str(datetime.datetime.now()) : traceback.format_exc()})
            print('Apologies, an error occurred.\nPlease check the logs for more information after the session is over.')
            if input('Continue Session? [y/n]') == 'y':
                 self.run()
            else:
                self.global_driver._write_logs(self.save_dir)

    def _process_responses(self, menu: Menu, driver: Driver):
        """
        Process the user's responses in the LNLPCLI command-line interface.

        Args:
            menu (Menu): The current menu being displayed.
            driver (Driver): The driver object for the LNLPCLI session.
        """
        response = driver._process_response(menu)

        if isinstance(response, list):
            driver.log("data", {str(menu): response})
        else:
            driver.log("data", {str(menu): str(response)})

        if isinstance(response, Menu):
            if not isinstance(response, (Landing, TopicMenu, OptimizationMenu)):
                response.set_parent(menu)

            self._process_responses(response, driver)

        elif isinstance(response, BERTopic):
            if self.global_session.config_topic_model != {}:
                self.tm_driver._run_topic_model(from_file=True)
            else:
                self.tm_driver._run_topic_model()
        
        elif isinstance(response, FineTuner):
            if self.global_session.config_fine_tune != {}:
                self.tu_driver._run_tuner(from_file=True)
            else:
                self.tu_driver._run_tuner()

        else:
            self._process_responses(menu.parent, driver)

    def _process_sequence(self, sequence: str):
        """
        Process a sequence of choices in the LNLPCLI command-line interface.

        Args:
            sequence (str): The sequence of commands to process.


        Example:
            sequence = '1,11,21,31,41,9'
                1: Run a Topic Model
                1: Select LLM to generate Embeddings
                    1: all-MiniLM-L6-v2
                2: Select Dimensionality Reduction Technique
                    1: UMAP
                3: Select Clustering Technique
                    1: HDBSCAN
                4: Fine Tuning
                    1: Enable 2 grams
                9: Run Topic Model

            python main.py --sequence='1,11,21,31,41,9'
        """
        if self.save_dir is None:
            self.save_dir = "output"
        
        self.global_driver.log("data", {"Topic": self.save_dir})

        sequence = sequence.split(",")

        sequence = [int(x) for x in sequence]

        self.landing = Landing(session=self.global_driver.session)

        choice = self.landing.handle_choice(sequence[0])

        for s in sequence[1:]:
            if s > 9:
                first_choice = floor(s / 10)
                menu = choice.handle_choice(first_choice)
                second_choice = s % 10
                response = menu.handle_choice(second_choice)
                
                if isinstance(response, list):
                    self.global_driver.log("data", {str(menu): response})
                else:
                    self.global_driver.log("data", {str(menu): str(response)})
            else:
                choice = choice.handle_choice(s) 
        
        if isinstance(choice, BERTopic):
            if self.global_session.config_topic_model != {}:
                self.tm_driver._run_topic_model(from_file=True)
            else:
                self.tm_driver._run_topic_model()
        
        elif isinstance(choice, FineTuner):
            if self.global_session.config_fine_tune != {}:
                self.tu_driver._run_tuner(from_file=True)
            else:
                self.tu_driver._run_tuner()