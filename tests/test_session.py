from util._session import Session
from loading._dataloader import DataLoader

def test_session_initialization():
    session = Session()
    assert session.data == []
    assert session.config_topic_model == {}
    assert session.config_optimization == {}
    assert session.logs == {"errors": [], "info": [], "data": []}
    assert session.plot_dir is None
    assert session.topic_model_factory.data is None


def test_session_initialization_with_data():
    data = [1, 2, 3]
    session = Session(data=data)
    assert session.data == data
    assert session.config_topic_model == {}
    assert session.config_optimization == {}
    assert session.logs == {"errors": [], "info": [], "data": []}
    assert session.plot_dir is None
    assert session.topic_model_factory.data is None


def test_session_initialization_with_configs():
    config_topic_model = {"param1": "value1", "param2": "value2"}
    config_optimization = {"param3": "value3", "param4": "value4"}
    session = Session(
        config_topic_model=config_topic_model, config_optimization=config_optimization
    )
    assert session.data == []
    assert session.config_topic_model == config_topic_model
    assert session.config_optimization == config_optimization
    assert session.logs == {"errors": [], "info": [], "data": []}
    assert session.plot_dir is None
    assert session.topic_model_factory.data is None


def test_session_logs():
    session = Session()
    assert session.logs == {"errors": [], "info": [], "data": []}

    session.logs["errors"].append("Error 1")
    session.logs["errors"].append("Error 2")

    session.logs["info"].append("Info 1")
    session.logs["info"].append("Info 2")

    session.logs["data"].append("Data 1")
    session.logs["data"].append("Data 2")

    assert session.logs == {
        "errors": ["Error 1", "Error 2"],
        "info": ["Info 1", "Info 2"],
        "data": ["Data 1", "Data 2"],
    }


def test_session_topic_model_factory():
    session = Session()
    assert session.topic_model_factory.data is None

    data = [
        "This is the first document.",
        "This document is the second document.",
        "And this is the third one.",
        "Is this the first document?",
    ]
    session.set_data(data)
    assert session.data == data

    session.initialize_topic_model_factory()
    assert session.topic_model_factory.data is not None


def test_set_config():
    session = Session()
    config = {"param1": "value1", "param2": "value2"}
    session.set_config_topic_model(config)
    assert session.config_topic_model == config

    config = {"param3": "value3", "param4": "value4"}
    session.set_config_optimization(config)
    assert session.config_optimization == config

def test_log_build_sync_no_file():
    session = Session()
    session.logs["data"].append({"Embeddings": "all-MiniLM-L12-v2"})
    session.logs["data"].append({"Dimensionality Reduction": "umap"})
    session.logs["data"].append({"Clustering": "hdbscan"})
    session.logs["data"].append({"Fine Tuning": "Enable 2-grams"})
    assert session.logs["data"] == [
        {"Embeddings": "all-MiniLM-L12-v2"},
        {"Dimensionality Reduction": "umap"},
        {"Clustering": "hdbscan"},
        {"Fine Tuning": "Enable 2-grams"},
    ]
    assert session.build_topic_model() is not None

def test_log_build_sync_with_file():
    loader = DataLoader()

    tm_config = loader._load_config("tests/test_data/config-tm.json")

    session = Session(config_topic_model=tm_config)

    assert session.build_topic_model(from_file=True, config=tm_config) is not None
