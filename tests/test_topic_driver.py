import json
import os
import pytest
from bertopic import BERTopic
from drivers._tm_driver import TopicDriver
from util._formatter import DataFormatter
import pandas as pd

def test_save_zipf_distribution(tmpdir):
    driver = TopicDriver()
    session_data = pd.DataFrame({
        "label": ["A", "A", "B", "B"],
        "text": ["text1", "text2", "text3", "text4"]
    })
    directory = str(tmpdir)
    formatter = DataFormatter() 
    driver._save_zipf_distribution(session_data, directory, formatter)

    assert os.path.isdir(f"{directory}/topics/")
    assert os.path.isfile(f"{directory}/topics/A_zipf.csv")
    assert os.path.isfile(f"{directory}/topics/A_sample_zipf.csv")
    assert os.path.isfile(f"{directory}/topics/B_zipf.csv")
    assert os.path.isfile(f"{directory}/topics/B_sample_zipf.csv")

    os.remove(f"{directory}/topics/A_zipf.csv")
    os.remove(f"{directory}/topics/A_sample_zipf.csv")
    os.remove(f"{directory}/topics/B_zipf.csv")
    os.remove(f"{directory}/topics/B_sample_zipf.csv")
    os.rmdir(f"{directory}/topics/")

def test_save_topic_model_config(tmpdir):
    driver = TopicDriver()
    directory = str(tmpdir)
    driver.initialize_session(data_path='tests/test_data/brazil-vaccine-comments.csv',save_dir=directory)
    driver.session.config_topic_model = {"n_gram_range": (1, 2)}
    driver._save_topic_model_config(directory)

    assert os.path.isfile(f"{directory}/tm_config.json")

    with open(f"{directory}/tm_config.json", "r") as f:
        config = json.load(f)

    assert config == {"n_gram_range": [1, 2]}

    os.remove(f"{directory}/tm_config.json")

def test_save_session_data(tmpdir):
    driver = TopicDriver()
    session_data = pd.DataFrame({
        "label": ["A", "A", "B", "B"],
        "text": ["text1", "text2", "text3", "text4"]
    })
    directory = str(tmpdir)
    driver._save_session_data(session_data, directory)

    assert os.path.isfile(f"{directory}/labeled_corpus.csv")

    data = pd.read_csv(f"{directory}/labeled_corpus.csv")

    assert data.equals(session_data)

    os.remove(f"{directory}/labeled_corpus.csv")

def test_reduce_embeddings_no_reduction():
    embeddings = pd.DataFrame({
        "x": [1, 2, 3],
        "y": [4, 5, 6]
    })

    driver = TopicDriver()
    reduced_embeddings = driver._reduce_embeddings_dimensions(embeddings)

    assert reduced_embeddings.equals(embeddings)

def test_reduce_embeddings_with_reduction_pass():
    embeddings = pd.DataFrame({
        "x": [1, 2, 3, 4],
        "y": [5, 6, 7, 8],
        "z": [9, 10, 11, 12]
    })

    driver = TopicDriver()
    reduced_embeddings = driver._reduce_embeddings_dimensions(embeddings)

    assert reduced_embeddings.shape == (4, 2)

def test_reduce_embeddings_with_reduction_fail():
    embeddings = pd.DataFrame({
        "x": [1, 2],
        "y": [5, 6],
        "z": [9, 10]
    })

    driver = TopicDriver()
    with pytest.raises(ValueError):
        reduced_embeddings = driver._reduce_embeddings_dimensions(embeddings)

def test_map_topics_to_documents(tmpdir):
    driver = TopicDriver()
    directory = str(tmpdir)
    driver.initialize_session(data_path='tests/test_data/brazil-vaccine-comments.csv',save_dir=directory)

    bertopic = BERTopic()

    docs = ["This is a test document.", "This is another test document.", "This is a third test document.",
            "This is a fourth test document.", "This is a fifth test document.", "This is a sixth test document.",
            "This is a seventh test document.", "This is an eighth test document.", "This is a ninth test document.",
            "This is a tenth test document."]
    driver.session.data = docs
    topics = bertopic.fit_transform(docs)[0]
    session_data, embeddings = driver._map_topics_to_documents(topics, bertopic)

    assert session_data.shape == (10, 2)
    assert embeddings.shape == (10, 384)

