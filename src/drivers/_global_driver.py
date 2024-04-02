from src.drivers._driver import Driver
from src.viz._tm_viz import visualize
from src.util._formatter import DataFormatter
from util._session import Session
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bertopic import BERTopic
import json
import os
import sys

class GlobalDriver(Driver):
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
            dummy = self._process_topic_choice(model, value, topics)
            if dummy != "":
                directory = dummy

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

    def _process_topic_choice(self, model: BERTopic, value: str, topics):
        """
        Processes the topic choice and saves the results.

        Args:
            model (BERTopic): The topic model object.
            value (str): The topic choice value.
            topics (list): The extracted topics.

        Returns:
            str: The directory where the results are saved.
        """
        directory = ""

        if self.session.plot_dir != "":
            directory = self.session.plot_dir
        if value.startswith("save_dir"):
            directory = value.split(" ")[1].strip()
        # if directory does not exist, create it
        if not os.path.isdir(directory):
            os.makedirs(directory)
        # model.save(directory, serialization="pytorch", save_embedding_model=True)
        # map topics to the documents

        topics = pd.DataFrame(topics).astype(int)
        # name the columns
        topics.columns = ["label"]
        embeddings = pd.DataFrame(model._extract_embeddings(self.session.data))
        session_data = pd.DataFrame(self.session.data)
        # name column text
        session_data.columns = ["text"]
        session_data = pd.concat([session_data, topics], axis=1)
        # map embeddings to the documents
        # if embeddings dim is more than 2, reduce to 2
        if embeddings.shape[1] > 2:
            from umap import UMAP

            umap = UMAP(n_components=2, verbose=True)
            embeddings = pd.DataFrame(umap.fit_transform(embeddings))
            # columns names are x and y
            embeddings.columns = ["x", "y"]
        session_data = pd.concat([session_data, embeddings], axis=1)

        pd.DataFrame(session_data).to_csv(
            f"{directory}/labeled_corpus.csv", index=False
        )
        tm_config = self.session.config_topic_model
        # save the topic model configuration
        if tm_config != {}:
            with open(f"{directory}/tm_config.json", "w") as f:
                json.dump(tm_config, f)

        formatter = DataFormatter()

        #size distribution of labels
        label_distribution = session_data["label"].value_counts().reset_index()

        plt.scatter(np.log10(list(range(len(label_distribution)))), np.log10(label_distribution["count"]))
        plt.title("Topic Size Distribution")
        plt.xlabel("log rank")
        plt.ylabel("log size")
        plt.savefig(f"{directory}/topic_size_distribution.png")

        for label in session_data["label"].unique():
            data = session_data[session_data["label"] == label]
            if len(data) > 1:
                if not os.path.isdir(f"{directory}/topics/"):
                    os.makedirs(f"{directory}/topics/")
                df = formatter.zipf_data_to_dataframe(data["text"].tolist())

                # sample of session_data size of df
                sample = session_data.sample(n=len(data) - 1)

                sample = formatter.zipf_data_to_dataframe(sample["text"].tolist())

                df.to_csv(f"{directory}/topics/{label}_zipf.csv", index=False)

                sample.to_csv(
                    f"{directory}/topics/{label}_sample_zipf.csv", index=False
                )

        return directory

    def _write_logs(self, directory):
        """
        Writes the logs to a JSON file.

        Args:
            directory (str): The directory where the logs should be saved.
        """
        errors = self.session.get_logs("errors")
        data = self.session.get_logs("data")
        logs = {"errors": errors, "data": data}
        if directory != "":
            with open(f"{directory}/logs.json", "w") as f:
                json.dump(logs, f)
        else:
            with open(f"logs.json", "w") as f:
                json.dump(logs, f)
