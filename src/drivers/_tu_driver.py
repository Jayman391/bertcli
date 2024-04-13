from src.drivers._driver import Driver
from util._session import Session

class TunerDriver(Driver):

  def __init__(self, session: Session = None):
    super().__init__(session)

  def _run_tuner(self, from_file: bool = False):
    data = self.session.get_logs("data")
    data = [log for log in data if "Back" not in log.values()]

    tuner = self.session.build_tuner(from_file=from_file)

    tuner.run()

