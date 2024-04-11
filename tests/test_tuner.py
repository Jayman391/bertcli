import sys
import os

# Add the source directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


from obj._tuner import Tuner
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
    
def test_tuner_run():
    model_filepath = 'models/model.pt'
    data_filepath = 'data/data.csv'
    prompt = 'Enter a sentence:'
    training_params = {'epochs': 10, 'batch_size': 32}

    tuner = Tuner(model_filepath, data_filepath, prompt, training_params)

    # Add your test logic here
    tuner.run()
    assert tuner.model_filepath == model_filepath
    assert tuner.data_filepath == data_filepath
    assert tuner.prompt == prompt
    assert tuner.training_params == training_params