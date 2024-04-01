from src.drivers._driver import Driver
from src.viz._tm_viz import visualize
from src.util._formatter import DataFormatter
from util._session import Session
from webbrowser import open_new_tab
from bertopic import BERTopic
import pandas as pd

import json
import os
import sys


class GlobalDriver(Driver):

    def __init__(self, session: Session = None):
        if sys.platform.startswith("linux"):
            self.file = ""
        else:
            self.file = "file://"
        super().__init__(session)

    def _run_topic_model(self, from_file: bool = False):
        try:
            data = self.session.logs["data"]
            directory = ""
            # remove all logs that containg Back in the values
            data = [log for log in data if "Back" not in log.values()]
            # gather data where Topic is a key
            topic_choices = [log for log in data if "Topic" in log.keys()]

            model = self.session.build_topic_model(from_file=from_file)
            self.session.logs["info"].append("Topic Model has been built")
            topics = self._fit_model(model)

            for log in topic_choices:
                value = str(list(log.values())[0])
                dummy = self._process_topic_choice(model, value, topics)
                if dummy != "":
                    directory = dummy

            visualize(model, self.session, directory, data)

            self._write_logs(directory)
        except Exception as e:
            print(e)
            self.session.logs["errors"].append(str(e.with_traceback()))
            self._run_topic_model(from_file=from_file)
            self._write_logs(directory)
        except Exception as e:
            print(e)
            self.session.logs["errors"].append(str(e.with_traceback()))
            self._run_topic_model(from_file=from_file)

    def _fit_model(self, model):
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

        self.session.logs["info"].append("Topics have been extracted")

        return topics

    def _process_topic_choice(self, model: BERTopic, value: str, topics):
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
        with open(f"{directory}/tm_config.json", "w") as f:
            json.dump(tm_config, f)

        formatter = DataFormatter()

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
        info = self.session.logs["info"]
        errors = self.session.logs["errors"]
        data = self.session.logs["data"]
        logs = {"info": info, "errors": errors, "data": data}
        if directory != "":
            with open(f"{directory}/logs.json", "w") as f:
                json.dump(logs, f)
        else:
            with open(f"logs.json", "w") as f:
                json.dump(logs, f)
