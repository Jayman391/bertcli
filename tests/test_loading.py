import pytest

from loading._dataloader import DataLoader
from _nllpcli import NLLPCLI

loader = DataLoader()


@pytest.mark.parametrize(
    "data_filepath", ["tests/test_data/data.csv", "tests/test_data/data.json"]
)
def test_load_data(data_filepath):
    data = loader._load_data(data_filepath)
    """ 
    assert that the first 4 ids are
    63c6dfc9194f73dec4c8d7dd 
    63c6f5b9533170c4627fdfe8 
    63c6f5b6533170c462767e03 
    63c6f5b9533170c46280dcb5
    """
    if data_filepath.endswith(".csv"):
        assert (
            data["text"][0]
            == "We'd have the best vaccination program under her.\\n\\nVaccine, vaccine, vaccine, VAC-CIIIIIIIIIIIIIINE!"
        )
        assert (
            data["text"][1]
            == "I will be getting all the vaccines for my baby, I have all the vaccines and so does mybhusband so we don't listen to that non sense of not getting the babies vaccinated because they can get X and Y and Z from the vaccines.\\nIs your husband vaccinated or he doesn't have any vaccines?"
        )
        assert (
            data["text"][2]
            == "As others said, there’s no vaccine shedding with the covid vaccines. Vaccine shedding only happens with live vaccines. Mostly from the nasal spray flu vaccine "
        )
        assert (
            data["text"][3]
            == "Yes. Other vaccines that were a new at the time of release? Smallpox vaccine, polio vaccines, measles vaccine, etc.\\n \\n"
        )
    if data_filepath.endswith(".json"):
        assert (
            data["text"][0]
            == "We'd have the best vaccination program under her.\n\nVaccine, vaccine, vaccine, VAC-CIIIIIIIIIIIIIINE!"
        )
        assert (
            data["text"][1]
            == "I will be getting all the vaccines for my baby, I have all the vaccines and so does mybhusband so we don't listen to that non sense of not getting the babies vaccinated because they can get X and Y and Z from the vaccines.\nIs your husband vaccinated or he doesn't have any vaccines?"
        )
        assert (
            data["text"][2]
            == "As others said, there’s no vaccine shedding with the covid vaccines. Vaccine shedding only happens with live vaccines. Mostly from the nasal spray flu vaccine "
        )
        assert (
            data["text"][3]
            == "Yes. Other vaccines that were a new at the time of release? Smallpox vaccine, polio vaccines, measles vaccine, etc.\n \n"
        )


def test_load_config():
    config = loader._load_config("tests/test_data/config-tm.json")
    assert config is not None
    assert config is not None
    assert config["language"] == "english"
    assert config["top_n_words"] == 10
    assert config["nr_topics"] == 10
    assert config["min_topic_size"] == 10
    assert config["low_memory"] == False
    assert config["calculate_probabilities"] == False
    assert config["seed_topic_list"] == None
    assert config["zeroshot_topic_list"] == None
    assert config["zeroshot_min_similarity"] == 0.7
    assert config["embedding_model"] == "all-MiniLM-L12-v2"
    assert config["umap_model"] == {
        "n_neighbors": 15,
        "n_components": 5,
        "metric": "cosine",
    }
    assert config["hdbscan_model"] == {
        "min_cluster_size": 10,
        "min_samples": 1,
        "cluster_selection_epsilon": 0.5,
    }
    assert config["vectorizer_model"] == {
        "min_df": 0.05,
        "max_df": 0.95,
        "ngram_range": [1, 2],
        "max_features": 10000,
    }
    assert config["ctfidf_model"] == {
        "bm25_weighting": True,
        "reduce_frequent_words": True,
    }
    assert config["representation_model"] == {
        "ZeroShotClassification": {
            "topics": ["business", "entertainment", "politics", "sport", "tech"],
            "model": "sentence-transformers/all-MiniLM-L12-v2",
        },
        "MaximalMarginalRelevance": {"diversity": 0.3},
    }
    assert config["verbose"] == True
    assert config["seed"] == 42


@pytest.mark.parametrize(
    "data_filepath", ["tests/test_data/data.csv", "tests/test_data/data.json"]
)
@pytest.mark.parametrize("config_filepath", ["tests/test_data/config-tm.json"])
@pytest.mark.parametrize("opt_filepath", ["tests/test_data/config-opt.json"])
def test_handle_globals(data_filepath, config_filepath, opt_filepath):
    cli = NLLPCLI(data_filepath, config_filepath, opt_filepath, True)

    assert cli.global_session.data is not None
    assert cli.global_session.config_topic_model is not None
    assert cli.global_session.config_optimization is not None


def test_invalid_filetype():
    with pytest.raises(Exception):
        cli = NLLPCLI("tests/test_data/data.txt")


def test_invalid_config_file():
    with pytest.raises(Exception):
        cli = NLLPCLI("tests/test_data/data.csv", "tests/test_data/config.txt")
