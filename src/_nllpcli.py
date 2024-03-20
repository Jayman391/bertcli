from src.drivers._global_driver import GlobalDriver
from src.drivers._tm_driver import TopicModelDriver
from src.menus._menu import Menu
from src.menus._landing import Landing
from src.menus.topic._topic import TopicMenu
from src.menus.optimization._optimization import OptimizationMenu
class NLLPCLI:
    def __init__(
        self,
        global_data_path: str = None,
        global_config_path: str = None,
        global_optmization_path: str = None,
        debug: bool = False,
    ):
        self.debug = debug
        self.global_data_path = global_data_path
        self.global_config_path = global_config_path
        self.global_optmization_path = global_optmization_path

        print("\nWelcome to the BERTopic CLI!")

        self.run()

    def run(self):
        self.driver = GlobalDriver()

        self.global_session = self.driver.initialize_session(
            data_path=self.global_data_path,
            config_path=self.global_config_path,
            optimization_path=self.global_optmization_path,
        )
        self.driver.log("info", "Initialized Global Session Object and Global Driver")

        self.landing = Landing(session=self.driver.session)
        self.driver.log("info", "Initialized Landing Menu")

        if self.debug:
            self.landing.handle_choice(1)
            return 

        response = self.driver.run_menu(self.landing)
        self.driver.log("info", f"User chose {response}")

        if isinstance(response, TopicMenu):
            self._run_topic()
        else:
            pass
    
    def _run_topic(self):
        self.topic_driver = TopicModelDriver(session=self.global_session)
        self.topic_driver.log("info", "Initialized Topic Model Driver")

        self.topic_menu = TopicMenu(self.topic_driver.session, self.landing)
        self.topic_driver.log("info", "Initialized Topic Menu")
        self.topic_menu.parent = self.landing

        menu = self.topic_menu
        while True:
            self._process_choices(menu)
            
    def _process_choices(self, menu: Menu):
        choice = self.topic_driver.run_menu(menu)

        response = self.topic_driver.process_response(choice)

        if isinstance(response, TopicMenu):
            self._run_topic()
        else:
            if isinstance(response, Menu):
                menu = response
            else:
                self.topic_driver.log("data", {choice: response})

