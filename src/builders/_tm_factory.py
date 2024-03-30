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

# set TOKENIZERS_PARALLELISM to False to avoid issues with transformers
import os

os.environ["TOKENIZERS_PARALLELISM"] = "False"

from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer

from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance, ZeroShotClassification, PartOfSpeech


class TopicModelFactory:
    def __init__(self):
        self.data = None
        # Step 1 - Extract embeddings
        self.embedding_model = None
        # Step 2 - Reduce dimensionality
        self.dimension_reduction_model = None
        # Step 3 - Cluster reduced embeddings
        self.clustering_model = None
        # Step 4 - Tokenize topics
        self.vectorizer_model = None
        # Step 5 - Create topic self.fine_tune
        self.ctfidf_model = None
        self.config = {}

    def upload_data(self, data: pd.DataFrame = None):
        if data is None:
            data = pd.read_csv("tests/test_data/data.csv")
        self.data = data
        return self.data

    def build_embedding_model(self, model: str = ""):
        if model == "":
            model = "all-MiniLM-L6-v2"
        self.embedding_model = SentenceTransformer(model)
        return self.embedding_model

    def build_dim_red_model(self, model: str = "", config: dict = {}):
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
        self.vectorizer_model = CountVectorizer(**config)
        return self.vectorizer_model

    def build_ctfidf_model(self, config: dict = {}):
        self.ctfidf_model = ClassTfidfTransformer(**config)
        return self.ctfidf_model
    
    def build_fine_tune(self, tune: list = []):
        self.fine_tune = []
        for log in tune:
            if isinstance(log, list):
                for word in log:
                    iszero = False
                    if word == "Zero Shot":
                        iszero = True
                        log.drop(word)
                if iszero:
                    self.fine_tune.append(ZeroShotClassification(candidate_topics=log))
            if log == "Enable KeyBERT algorithm":
                self.fine_tune.append(KeyBERTInspired())
            if log == "Enable Maximal Marginal Relevance":
                self.fine_tune.append(MaximalMarginalRelevance(1))
            if log == "Enable Part of Speech filtering":
                self.fine_tune.append(PartOfSpeech("en_core_web_sm"))

        return self.fine_tune

    def build_topic_model(self, config: dict = {}) -> BERTopic:
        print(self.fine_tune)
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
