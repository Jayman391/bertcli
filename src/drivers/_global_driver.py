from src.drivers._driver import Driver
from src.menus._menu import Menu
from src.menus._landing import Landing
from util._session import Session
 
class GlobalDriver(Driver):
    def __init__(self, session:Session = None):
        super().__init__(session)        
    
        