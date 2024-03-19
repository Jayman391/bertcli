from src.drivers._driver import Driver
from src.menus._menu import Menu
from src.menus._landing import Landing
 
class GlobalDriver(Driver):
    def __init__(self):
        super().__init__()
        self.data = {}

   
