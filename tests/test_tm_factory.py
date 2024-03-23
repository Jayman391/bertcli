import pytest
import pandas as pd
from builders._tm_factory import TopicModelFactory


@pytest.fixture
def sample_data():
    # Create a sample DataFrame for testing
    data = pd.DataFrame(
        {
            "text": [
                "This is the first document.",
                "This document is the second document.",
                "And this is the third one.",
                "Is this the first document?",
            ]
        }
    )
    return data


def test_build_embedding_model(sample_data):
    factory = TopicModelFactory()
    factory.upload_data(sample_data)
    embedding_model = factory.build_embedding_model(
        "sentence-transformers/all-MiniLM-L12-v2"
    )
    assert embedding_model is not None
    assert factory.embedding_model == embedding_model


def test_build_dim_red_model(sample_data):
    factory = TopicModelFactory()
    factory.upload_data(sample_data)
    dim_red_model = factory.build_dim_red_model(
        "umap", {"n_neighbors": 5, "n_components": 2}
    )
    assert dim_red_model is not None
    assert factory.dimension_reduction_model == dim_red_model


def test_build_cluster_model(sample_data):
    factory = TopicModelFactory()
    factory.upload_data(sample_data)
    cluster_model = factory.build_cluster_model("hdbscan", {"min_cluster_size": 5})
    assert cluster_model is not None
    assert factory.clustering_model == cluster_model


def test_build_vectorizer_model(sample_data):
    factory = TopicModelFactory()
    factory.upload_data(sample_data)
    vectorizer_model = factory.build_vectorizer_model({"max_features": 1000})
    assert vectorizer_model is not None
    assert factory.vectorizer_model == vectorizer_model


def test_build_ctfidf_model(sample_data):
    factory = TopicModelFactory()
    factory.upload_data(sample_data)
    ctfidf_model = factory.build_ctfidf_model({"bm25_weighting": True})
    assert ctfidf_model is not None
    assert factory.ctfidf_model == ctfidf_model


def test_build_topic_model(sample_data):
    factory = TopicModelFactory()
    factory.upload_data(sample_data)
    factory.build_embedding_model("sentence-transformers/all-MiniLM-L12-v2")
    factory.build_dim_red_model("umap", {"n_neighbors": 5, "n_components": 2})
    factory.build_cluster_model("hdbscan", {"min_cluster_size": 5})
    factory.build_vectorizer_model({"max_features": 1000})
    factory.build_ctfidf_model({"bm25_weighting": True})
    topic_model = factory.build_topic_model()
    assert topic_model is not None
