from src.drivers._driver import Driver
from src.drivers._global_driver import GlobalDriver
from src.menus._menu import Menu
from src.menus._landing import Landing
from src.menus.topic._topic import TopicMenu
from src.menus.optimization._optimization import OptimizationMenu
from bertopic import BERTopic


class LNLPCLI:
    def __init__(
        self,
        save_dir: str = None,
        global_data_path: str = None,
        global_config_path: str = None,
        global_optmization_path: str = None,
        num_samples:int = 0,
        num_samples:int = 0,
        debug: bool = False,
    ):
        self.debug = debug
        self.global_data_path = global_data_path
        self.global_config_path = global_config_path
        self.global_optmization_path = global_optmization_path
        self.num_samples = num_samples
        self.save_dir = save_dir

        print("\nWelcome to the LNLP CLI!")

        self.driver = GlobalDriver()

        self.global_session = self.driver.initialize_session(
            data_path=self.global_data_path,
            config_path=self.global_config_path,
            optimization_path=self.global_optmization_path,
            num_samples=self.num_samples,
            save_dir=self.save_dir,
        )

        self.driver.log("info", "Initialized Global Session Object and Global Driver")

    def run(self):
        try:
            self.landing = Landing(session=self.driver.session)

            if self.debug:
                self.landing.handle_choice(1)
                return

            for _, value in self.landing.menus.items():
                if value is not None and isinstance(value, Menu):
                    value.set_parent(self.landing)

            self._process_responses(self.landing, self.driver)
        except Exception as e:
            self.driver.log("error", str(e))
            print("An error occurred. Please try again.")
            trace = input("Would you like to see the error trace? (y/n): ")
            if trace.lower() == "y":
                print(e.with_traceback())
            self.run()

    def _process_responses(self, menu: Menu, driver: Driver):
        response = driver._process_response(menu)

        if isinstance(response,list):

            driver.log("data", {str(menu): response})
        else:
            driver.log("data", {str(menu): str(response)})
        if isinstance(response,list):

            driver.log("data", {str(menu): response})
        else:
            driver.log("data", {str(menu): str(response)})

        if isinstance(response, Menu):

            if not isinstance(response, (Landing, TopicMenu, OptimizationMenu)):
                response.set_parent(menu)

            self._process_responses(response, driver)

        elif isinstance(response, BERTopic):
            
            
            if self.global_session.config_topic_model != {}:
                driver._run_topic_model(from_file=True)
            else:
                driver._run_topic_model()
        else:
            self._process_responses(menu.parent, driver)
