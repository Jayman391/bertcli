from src.util._session import Session
from src.drivers._driver import Driver
from src.drivers._global_driver import GlobalDriver
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
        
        for _, value in self.landing.menus.items():
            if value is not None and isinstance(value, Menu):
                value.set_parent(self.landing)

        self._process_responses(self.landing, self.driver)
            
    def _process_responses(self, menu: Menu, driver:Driver):
      
        response = driver.process_response(menu)

        driver.log("data", {menu: response})
        print(driver.session.logs["data"])

        if isinstance(response, Menu):
            if not isinstance(response, (Landing, TopicMenu, OptimizationMenu)):
                response.set_parent(menu)
            self._process_responses(response, driver)
        else:
            self._process_responses(menu.parent, driver)
