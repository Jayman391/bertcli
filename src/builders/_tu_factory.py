from src.obj._finetuner import FineTuner

class TunerFactory:
  @staticmethod
  def create_tuner(model_filepath:str = '', data_filepath:str = '', prompt:str = '',output_path:str = '', training_params:dict = ''):
    return FineTuner(model_filepath, data_filepath, prompt, output_path, training_params)
  