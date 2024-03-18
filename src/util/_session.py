from src.builders._tm_factory import TopicModelFactory

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

    self.topic_model_factory = TopicModelFactory()

  def set_data(self, data):
    self.data = data
    return self.data
  
  def set_config_topic_model(self, config):
    self.config_topic_model = config
    return self.config_topic_model
  
  def set_config_optimization(self, config):
    self.config_optimization = config
    return self.config_optimization

  def initialize_topic_model_factory(self):
    self.topic_model_factory.upload_data(self.data)
    return self.topic_model_factory