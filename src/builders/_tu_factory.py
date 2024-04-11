from src.obj._tuner import Tuner

class TunerFactory:
  @staticmethod
  def create_tuner(model_filepath:str = '', data_filepath:str = '', prompt:str = '', training_params:dict = ''):
    return Tuner(model_filepath, data_filepath, prompt, training_params)
  