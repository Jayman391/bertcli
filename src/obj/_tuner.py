class Tuner:
  def __init__(self, model_filepath = '', data_filepath = '', prompt = '', training_params:dict = {}):
    self.model_filepath = model_filepath
    self.data_filepath = data_filepath
    self.prompt = prompt
    self.training_params = training_params

  def run(self):
    pass