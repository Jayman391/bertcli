import pandas as pd

from umap import UMAP
from sklearn.decomposition import PCA, TruncatedSVD, FastICA

from hdbscan import HDBSCAN
from sklearn.cluster import (
    KMeans,
    SpectralClustering,
    DBSCAN,
    AgglomerativeClustering,
    Birch,
    AffinityPropagation,
    MeanShift,
)
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from transformers import pipeline

# set TOKENIZERS_PARALLELISM to False to avoid issues with transformers
import os

os.environ["TOKENIZERS_PARALLELISM"] = "False"

from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer

from bertopic.representation import (
    KeyBERTInspired,
    MaximalMarginalRelevance,
    ZeroShotClassification,
    PartOfSpeech,
    TextGeneration,
    LangChain
)

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

class TopicModelFactory:
    """
    A factory class for building a topic model using various steps and models.

    Attributes:
        data (pd.DataFrame): The input data for the topic model.
        embedding_model: The model used for extracting embeddings.
        dimension_reduction_model: The model used for reducing dimensionality.
        clustering_model: The model used for clustering reduced embeddings.
        vectorizer_model: The model used for tokenizing topics.
        ctfidf_model: The model used for creating topic self.fine_tune.
        config (dict): Additional configuration parameters for the topic model.

    Methods:
        upload_data: Uploads the input data for the topic model.
        build_embedding_model: Builds the embedding model.
        build_dim_red_model: Builds the dimensionality reduction model.
        build_cluster_model: Builds the clustering model.
        build_vectorizer_model: Builds the vectorizer model.
        build_ctfidf_model: Builds the ctfidf model.
        build_fine_tune: Builds the fine-tuning models.
        build_topic_model: Builds the final topic model.

    """

    def __init__(self):
        self.data = None
        self.embedding_model = None
        self.dimension_reduction_model = None
        self.clustering_model = None
        self.vectorizer_model = None
        self.ctfidf_model = None
        self.config = {}
        self.fine_tune = []

    def upload_data(self, data: pd.DataFrame = None):
        """
        Uploads the input data for the topic model.

        Args:
            data (pd.DataFrame, optional): The input data as a pandas DataFrame. If not provided, it will be read from a default file.

        Returns:
            pd.DataFrame: The uploaded data.

        """
        if data is None:
            data = pd.read_csv("tests/test_data/data.csv")
        self.data = data
        return self.data

    def build_embedding_model(self, model: str = ""):
        """
        Builds the embedding model.

        Args:
            model (str, optional): The name of the embedding model to use. If not provided, a default model will be used.

        Returns:
            The built embedding model.

        """
        if model == "" or model == "Back":
            model = "all-MiniLM-L6-v2"
        self.embedding_model = SentenceTransformer(model)
        return self.embedding_model

    def build_dim_red_model(self, model: str = "", config: dict = {}):
        """
        Builds the dimensionality reduction model.

        Args:
            model (str, optional): The name of the dimensionality reduction model to use. If not provided, a default model will be used.
            config (dict, optional): Additional configuration parameters for the model.

        Returns:
            The built dimensionality reduction model.

        """
        model = model.lower()
        if model == "umap" or model == "":
            self.dimension_reduction_model = UMAP(
                init="tswspectral", verbose=True, **config
            )

        if model == "pca":
            self.dimension_reduction_model = PCA(**config)

        if model == "truncated svd":
            self.dimension_reduction_model = TruncatedSVD(**config)

        if model == "independent component analysis":
            self.dimension_reduction_model = FastICA(**config)

        return self.dimension_reduction_model

    def build_cluster_model(self, model: str = "", config: dict = {}):
        """
        Builds the clustering model.

        Args:
            model (str, optional): The name of the clustering model to use. If not provided, a default model will be used.
            config (dict, optional): Additional configuration parameters for the model.

        Returns:
            The built clustering model.

        """
        model = model.lower()
        if model == "hdbscan" or model == "":
            self.clustering_model = HDBSCAN(**config)

        if model == "kmeans":
            self.clustering_model = KMeans(**config)

        if model == "spectral clustering":
            self.clustering_model = SpectralClustering(**config)

        if model == "dbscan":
            self.clustering_model = DBSCAN(**config)

        if model == "agglomerative clustering":
            self.clustering_model = AgglomerativeClustering(**config)

        if model == "birch":
            self.clustering_model = Birch(**config)

        if model == "affinity propagation":
            self.clustering_model = AffinityPropagation(**config)

        if model == "mean shift":
            self.clustering_model = MeanShift(**config)

        return self.clustering_model

    def build_vectorizer_model(self, config: dict = {}):
        """
        Builds the vectorizer model.

        Args:
            config (dict, optional): Additional configuration parameters for the model.

        Returns:
            The built vectorizer model.

        """
        self.vectorizer_model = CountVectorizer(**config)
        return self.vectorizer_model

    def build_ctfidf_model(self, config: dict = {}):
        """
        Builds the ctfidf model.

        Args:
            config (dict, optional): Additional configuration parameters for the model.

        Returns:
            The built ctfidf model.

        """
        self.ctfidf_model = ClassTfidfTransformer(**config)
        return self.ctfidf_model

    def build_fine_tune(self, tune: list = []):
        """
        Builds the fine-tuning models.

        Args:
            tune (list, optional): A list of fine-tuning models to enable.

        Returns:
            list: The built fine-tuning models.

        """
        self.fine_tune = []
        for log in tune:
            if isinstance(log, list):
                for word in log:
                    iszero = False
                    if word == "Zero Shot":
                        iszero = True
                        log.remove(word)
                if iszero:
                    zeroshot = ZeroShotClassification(candidate_topics=log)
                    self.fine_tune.append(zeroshot)
            if log == "Enable KeyBERT algorithm":
                self.fine_tune.append(KeyBERTInspired())
            if log == "Enable Maximal Marginal Relevance":
                self.fine_tune.append(MaximalMarginalRelevance(1))
            if log == "Enable Part of Speech filtering":
                self.fine_tune.append(PartOfSpeech())
            if log == "Enable Huggingface Text Generation":
                generator = pipeline('text2text-generation', model='google/flan-t5-base')
                self.fine_tune.append(TextGeneration(generator))
            
        return self.fine_tune

    def build_topic_model(self, config: dict = {}) -> BERTopic:
        """
        Builds the final topic model.

        Args:
            config (dict, optional): Additional configuration parameters for the topic model.

        Returns:
            BERTopic: The built topic model.

        """
        return BERTopic(
            embedding_model=self.embedding_model,
            umap_model=self.dimension_reduction_model,
            hdbscan_model=self.clustering_model,
            vectorizer_model=self.vectorizer_model,
            ctfidf_model=self.ctfidf_model,
            representation_model=self.fine_tune,
            verbose=True,
            **config
        )
