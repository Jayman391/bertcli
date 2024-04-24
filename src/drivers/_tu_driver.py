from src.drivers._driver import Driver
from util._session import Session


class TunerDriver(Driver):
    def __init__(self, session: Session = None):
        super().__init__(session)

    def _run_tuner(self, from_file: bool = False):
        tuner = self.session.build_tuner(from_file=from_file)

        tuner.run()
