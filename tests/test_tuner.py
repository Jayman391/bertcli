import sys
import os

# Add the source directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


from obj._finetuner import FineTuner
from builders._tu_factory import TunerFactory

def test_create_tuner():
    model_filepath = 'path/to/model'
    data_filepath = 'path/to/data'
    prompt = 'Sample prompt'
    training_params = {'param1': 'value1', 'param2': 'value2'}

    tuner = TunerFactory.create_tuner(model_filepath, data_filepath, prompt, training_params)

    assert tuner.model_filepath == model_filepath
    assert tuner.data_filepath == data_filepath
    assert tuner.prompt == prompt
    assert tuner.training_params == training_params