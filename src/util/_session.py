class Session:

  def __init__(self, data=None, config_topic_model=None, config_optimization=None) -> None:
    self.data = data
    self.config_topic_model = config_topic_model
    self.config_optimization = config_optimization
    self.logs = {
      "topic_model": [],
      "optimization": [],
      "errors": []
    }
    self.plot_dir = None