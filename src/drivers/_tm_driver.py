from src.drivers._driver import Driver
from src.viz._tm_viz import visualize
from src.util._formatter import DataFormatter
from util._session import Session
from transformers import pipeline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from umap import UMAP
import json
import os
import sys


class TopicDriver(Driver):
    """
    The GlobalDriver class is a subclass of the Driver class and represents a global driver for topic modeling.

    Attributes:
        session (Session): The session object associated with the driver.

    Methods:
        __init__(self, session=None): Initializes a new instance of the GlobalDriver class.
        _run_topic_model(self, from_file=False): Runs the topic modeling process.
        _fit_model(self, model): Fits the topic model to the session data and extracts the topics.
        _process_topic_choice(self, model, value, topics): Processes the topic choice and saves the results.
        _write_logs(self, directory): Writes the logs to a JSON file.
    """

    def __init__(self, session: Session = None):
        """
        Initializes a new instance of the GlobalDriver class.

        Args:
            session (Session, optional): The session object associated with the driver. Defaults to None.
        """
        if sys.platform.startswith("linux"):
            self.file = ""
        else:
            self.file = "file://"
        super().__init__(session)

    def _run_topic_model(self, from_file: bool = False):
        """
        Runs the topic modeling process.

        Args:
            from_file (bool, optional): Indicates whether to load data from a file. Defaults to False.
        """

        data = self.session.get_logs("data")
        directory = ""
        # remove all logs that contain "Back" in the values
        data = [log for log in data if "Back" not in log.values()]
        # gather data where "Topic" is a key
        topic_choices = [log for log in data if "Topic" in log.keys()]

        model = self.session.build_topic_model(from_file=from_file)
        topics = self._fit_model(model)

        for log in topic_choices:
            value = str(list(log.values())[0])
            save_dir = self._process_save_dir_choice(model, value, topics)
            if save_dir != "":
                directory = save_dir

        visualize(model, self.session, directory, data)

        self._write_logs(directory)

    def _fit_model(self, model):
        """
        Fits the topic model to the session data and extracts the topics.

        Args:
            model: The topic model object.

        Returns:
            list: The extracted topics.
        """
        topics, _ = model.fit_transform(self.session.data)
        # set -1 cluster to num_clusters+1
        num_topics = len(set(topics))

        topics = [
            (
                int(topic)
                if topic != -1 and isinstance(topic, bool) == False
                else int(num_topics)
            )
            for topic in topics
        ]

        return topics

    def _process_save_dir_choice(self, model, value, topics):
        """
        Processes the topic choice and saves the results.

        Args:
            model (BERTopic): The topic model object.
            value (str): The topic choice value.
            topics (list): The extracted topics.

        Returns:
            str: The directory where the results are saved.
        """
        # Setup directory for saving results
        directory = self._setup_directory(value)

        # Map topics to documents and process session data
        session_data, embeddings = self._map_topics_to_documents(topics, model)

        # Reduce embeddings dimensions if necessary
        embeddings = self._reduce_embeddings_dimensions(embeddings)
        session_data = pd.concat([session_data, embeddings], axis=1)

        session_data = self._label_text_with_sentiment(session_data)

        # Save the session data to CSV
        self._save_session_data(session_data, directory)

        # Save the topic model configuration
        self._save_topic_model_config(directory)

        # Plot and save the topic size distribution
        self._plot_topic_size_distribution(session_data, directory)

        # Save Zipf distribution for each topic and a sample
        formatter = DataFormatter()  # Assuming DataFormatter is defined elsewhere
        self._save_zipf_distribution(session_data, directory, formatter)

        return directory

    def _setup_directory(self, value):
        """
        Setup the directory for saving results.
        """
        directory = self.session.plot_dir if self.session.plot_dir != "" else ""
        if value.startswith("save_dir"):
            directory = value.split(" ")[1].strip()
        if not os.path.isdir(directory):
            os.makedirs(directory)
        return directory

    def _save_model(self, model, directory):
        """
        Save the model to the directory.
        """
        model.save(directory, serialization="pytorch", save_embedding_model=True)

    def _map_topics_to_documents(self, topics, model):
        """
        Process topics and map them to documents.
        """
        topics_df = pd.DataFrame(data=topics, columns=["label"]).astype(int)
        embeddings = pd.DataFrame(model._extract_embeddings(self.session.data))
        session_data = pd.DataFrame(self.session.data, columns=["text"])
        session_data = pd.concat([session_data, topics_df], axis=1)
        return session_data, embeddings

    def _reduce_embeddings_dimensions(self, embeddings):
        """
        Reduce the dimensionality of embeddings if necessary.
        """
        if embeddings.shape[1] > 2:
            umap = UMAP(n_components=2)
            embeddings = pd.DataFrame(
                umap.fit_transform(embeddings), columns=["x", "y"]
            )
        return embeddings

    def _save_session_data(self, session_data, directory):
        """
        Save the session data to a CSV file.
        """
        session_data.to_csv(f"{directory}/labeled_corpus.csv", index=False)

    def _label_text_with_sentiment(self, session_data):
        if self.session.sentiment != "":
            sentiment = pipeline(self.session.sentiment)
        else:
            sentiment = pipeline("sentiment-analysis")

        # for each entry in the "text" column, if any entry is too long, split it into smaller chunks and analyze sentiment and then pool
        # the sentiment scores
        for i, row in session_data.iterrows():
            if len(row["text"]) > 512:
                text = row["text"]
                chunks = [text[i : i + 512] for i in range(0, len(text), 512)]
                scores = [sentiment(chunk)[0]["score"] for chunk in chunks]
                session_data.at[i, "sentiment"] = sum(scores) / len(scores)
            else:
                session_data.at[i, "sentiment"] = sentiment(row["text"])[0]["score"]

        return session_data

    def _save_topic_model_config(self, directory):
        """
        Save the topic model configuration.
        """
        tm_config = self.session.config_topic_model
        if tm_config != {}:
            with open(f"{directory}/tm_config.json", "w") as f:
                json.dump(tm_config, f)

    def _plot_topic_size_distribution(self, session_data, directory):
        """
        Plot and save the topic size distribution.
        """
        label_distribution = session_data["label"].value_counts().reset_index()
        os.makedirs(directory, exist_ok=True)
        label_distribution.to_csv(
            f"{directory}/topic_size_distribution.csv", index=False
        )
        plt.scatter(
            np.log10(list(range(len(label_distribution["label"].unique())))),
            np.log10(sorted(label_distribution["count"])[::-1]),
        )
        plt.title("Topic Size Distribution")
        plt.xlabel("log rank")
        plt.ylabel("log size")
        plt.savefig(f"{directory}/topic_size_distribution.png")

    def _save_zipf_distribution(self, session_data, directory, formatter):
        """
        Save the Zipf distribution for each topic and a sample.
        """
        for label in session_data["label"].unique():
            data = session_data[session_data["label"] == label]
            if len(data) > 1:
                topic_dir = f"{directory}/topics/"
                if not os.path.isdir(topic_dir):
                    os.makedirs(topic_dir)
                df = formatter.zipf_data_to_dataframe(data["text"].tolist())
                sample = session_data.sample(n=len(data) - 1)
                sample_df = formatter.zipf_data_to_dataframe(sample["text"].tolist())
                df.to_csv(f"{topic_dir}/{label}_zipf.csv", index=False)
                sample_df.to_csv(f"{topic_dir}/{label}_sample_zipf.csv", index=False)
