from src.drivers._driver import Driver
from util._session import Session


class GlobalDriver(Driver):
    def __init__(self, session: Session = None):
        super().__init__(session)
