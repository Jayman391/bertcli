import pytest 

import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from main import BERTCLI

@pytest.mark.parametrize("filepath", ["tests/test_data/data.csv", "tests/test_data/data.json"])
def test_load_data(filepath):
    BERTcli = BERTCLI(filepath)
    assert BERTcli.global_session.data is not None
    assert BERTcli.global_session.config_topic_model == {}
    """ 
    assert that the first 4 ids are
    63c6dfc9194f73dec4c8d7dd 
    63c6f5b9533170c4627fdfe8 
    63c6f5b6533170c462767e03 
    63c6f5b9533170c46280dcb5
    """
    if filepath.endswith('.csv'):
        assert BERTcli.global_session.data['text'][0] == "We'd have the best vaccination program under her.\\n\\nVaccine, vaccine, vaccine, VAC-CIIIIIIIIIIIIIINE!"
        assert BERTcli.global_session.data['text'][1] == "I will be getting all the vaccines for my baby, I have all the vaccines and so does mybhusband so we don't listen to that non sense of not getting the babies vaccinated because they can get X and Y and Z from the vaccines.\\nIs your husband vaccinated or he doesn't have any vaccines?"
        assert BERTcli.global_session.data['text'][2] == "As others said, there’s no vaccine shedding with the covid vaccines. Vaccine shedding only happens with live vaccines. Mostly from the nasal spray flu vaccine "
        assert BERTcli.global_session.data['text'][3] == "Yes. Other vaccines that were a new at the time of release? Smallpox vaccine, polio vaccines, measles vaccine, etc.\\n \\n"
    if filepath.endswith('.json'):
        assert BERTcli.global_session.data['text'][0] == "We'd have the best vaccination program under her.\n\nVaccine, vaccine, vaccine, VAC-CIIIIIIIIIIIIIINE!" 
        assert BERTcli.global_session.data['text'][1] == "I will be getting all the vaccines for my baby, I have all the vaccines and so does mybhusband so we don't listen to that non sense of not getting the babies vaccinated because they can get X and Y and Z from the vaccines.\nIs your husband vaccinated or he doesn't have any vaccines?" 
        assert BERTcli.global_session.data['text'][2] == "As others said, there’s no vaccine shedding with the covid vaccines. Vaccine shedding only happens with live vaccines. Mostly from the nasal spray flu vaccine " 
        assert BERTcli.global_session.data['text'][3] == "Yes. Other vaccines that were a new at the time of release? Smallpox vaccine, polio vaccines, measles vaccine, etc.\n \n"

def test_load_config():
    BERTcli = BERTCLI("tests/test_data/data.csv", "tests/test_data/config.json")
    assert BERTcli.global_session.data is not None
    assert BERTcli.global_session.config_topic_model is not None
    assert BERTcli.global_session.config_topic_model['language'] == "english"
    assert BERTcli.global_session.config_topic_model['top_n_words'] == 10
    assert BERTcli.global_session.config_topic_model['nr_topics'] == 10
    assert BERTcli.global_session.config_topic_model['min_topic_size'] == 10
    assert BERTcli.global_session.config_topic_model['low_memory'] == False
    assert BERTcli.global_session.config_topic_model['calculate_probabilities'] == False 
    assert BERTcli.global_session.config_topic_model["seed_topic_list"] == None
    assert BERTcli.global_session.config_topic_model["zeroshot_topic_list"] == None
    assert BERTcli.global_session.config_topic_model["zeroshot_min_similarity"] ==  0.7
    assert BERTcli.global_session.config_topic_model["embedding_model"] ==  "all-MiniLM-L12-v2"
    assert BERTcli.global_session.config_topic_model["umap_model"] ==  {
        "n_neighbors": 15,
        "n_components": 5,
        "metric": "cosine"
    }
    assert BERTcli.global_session.config_topic_model["hdbscan_model"] ==  {
        "min_cluster_size": 10,
        "min_samples": 1,
        "cluster_selection_epsilon": 0.5
    }
    assert BERTcli.global_session.config_topic_model["vectorizer_model"] ==  {
        "min_df": 0.05,
        "max_df": 0.95,
        "ngram_range": [
        1,
        2
        ],
        "max_features": 10000
    }
    assert BERTcli.global_session.config_topic_model["ctfidf_model"] ==  {
        "bm25_weighting": True,
        "reduce_frequent_words": True
    }
    assert BERTcli.global_session.config_topic_model["representation_model"] == {
        "ZeroShotClassification" : {
        "topics" : [
            "business",
            "entertainment",
            "politics",
            "sport",
            "tech"] ,
        "model" : "sentence-transformers/all-MiniLM-L12-v2"
        },
        "MaximalMarginalRelevance" : {
        "diversity" : 0.3
        }
    }
    assert BERTcli.global_session.config_topic_model["verbose"] == True
    assert BERTcli.global_session.config_topic_model["seed" ] == 42

@pytest.mark.parametrize("data_filepath", ["tests/test_data/data.csv", "tests/test_data/data.json", None])
@pytest.mark.parametrize("config_filepath", ["tests/test_data/config.json", None])
def test_handle_globals(data_filepath, config_filepath):
    cli = BERTCLI(data_filepath, config_filepath)
    assert cli.global_session.data is not None
    assert cli.global_session.config_topic_model is not None

def test_invalid_filetype():
    with pytest.raises(Exception):
        cli = BERTCLI("tests/test_data/data.txt")

def test_invalid_config_file():
    with pytest.raises(Exception):
        cli = BERTCLI("tests/test_data/data.csv", "tests/test_data/config.txt")