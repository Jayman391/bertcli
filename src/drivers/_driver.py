from abc import ABC
from src.menus._menu import Menu
from src.loading._dataloader import DataLoader
from util._session import Session
import webbrowser
from webbrowser import open_new_tab
from bertopic import BERTopic
import pandas as pd
import os
import math
import json
import os
import sys

if sys.platform.startswith("linux"):
    file = ""
else:
    file = "file://"

class Driver(ABC):
    def __init__(self, session: Session = None):
        self._session: Session = session
        self._session_data = {}

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session):
        self._session = session

    @property
    def session_data(self):
        return self._session_data

    @session_data.setter
    def session_data(self, key, value):
        self._session_data[key] = value

    def initialize_session(
        self,
        data_path: str = None,
        config_path: str = None,
        optimization_path: str = None,
    ):
        loader = DataLoader()
        self.session = loader.initialize_session(
            data_path, config_path, optimization_path
        )

        return self.session

    def log(self, type: str, message: str):
        if type not in self.session.logs.keys():
            self.session.logs[type] = []

        self.session.logs[type].append(message)

        return {type: message}

    def run_menu(self, menu: Menu):
        menu.display()
        choice = menu.prompt_numeric("Choose an option: ")
        if choice < 1 or choice > len(menu.options):
            print("Invalid choice. Please choose a valid number.")
            choice = menu.prompt_numeric("Choose an option: ")
        response = menu.handle_choice(choice)

        return response

    def process_response(self, response):
        if isinstance(response, Menu):
            return self.run_menu(response)
        else:
            return response
    
    def run_topic_model(self, from_file: bool = False):
        model = self.session.build_topic_model(from_file=from_file)
        self.session.logs["info"].append("Topic Model has been built")

        topics, data = self._fit_model(model)

        directory = ""
        #remove all logs that containg Back in the values
        data = [log for log in data if "Back" not in log.values()]
        #gather data where Topic is a key
        topic_choices = [log for log in data if "Topic" in log.keys()]

        for log in topic_choices:
            value = str(list(log.values())[0])
            dummy = self._process_topic_choice(model, value, topics)
            if dummy:
                directory = dummy
            
        
        self._visualize(model, directory, data)

        self._write_logs(directory)

    def _fit_model(self, model):
        topics, _ = model.fit_transform(self.session.data)
        # set -1 cluster to num_clusters+1
        num_topics = len(set(topics))

        topics = [
            int(topic) if topic != -1 and isinstance(topic, bool) == False else int(num_topics)
            for topic in topics
        ]
        
        self.session.logs["info"].append("Topics have been extracted")
        data = self.session.logs["data"]
    
        return topics, data
    
    def _process_topic_choice(self, model:BERTopic, value: str, topics):
        if value.startswith("save_directory"):
                directory = value.split(" ")[1].strip()
                # if directory does not exist, create it
                if not os.path.isdir(directory):
                    os.makedirs(directory)
                model.save(directory, serialization="pytorch", save_embedding_model=True)
                #map topics to the documents
                  
                topics = pd.DataFrame(topics).astype(int)
                # name the columns
                topics.columns = ["labels"]
                embeddings = pd.DataFrame(model._extract_embeddings(self.session.data))
                session_data = pd.DataFrame(self.session.data)
                # name column text
                session_data.columns = ["text"]
                session_data = pd.concat([session_data, topics], axis=1)
                #map embeddings to the documents
                # if embeddings dim is more than 2, reduce to 2
                if embeddings.shape[1] > 2:
                    from umap import UMAP
                    umap = UMAP(n_components=2, verbose=True)
                    embeddings = pd.DataFrame(umap.fit_transform(embeddings))
                    # columns names are x and y
                    embeddings.columns = ["x", "y"]
                session_data = pd.concat([session_data, embeddings], axis=1) 
                
                pd.DataFrame(session_data).to_csv(f"{directory}/labeled_corpus.csv", index=False)
                tm_config = self.session.config_topic_model
                #save the topic model configuration
                with open(f"{directory}/tm_config.json", "w") as f:
                    json.dump(tm_config, f)

                return directory

    def _visualize(self, model: BERTopic, directory: str = "", data: list = []):
        plotting = [log for log in data if "Plotting" in log.keys()]
        self.session.logs["info"].append("Plotting Topics")
        if len(plotting) > 0:
            for log in plotting:
                value = str(list(log.values())[0])
                if (
                    str(value) == "firefox"
                    or value == "chrome"
                    or value == "safari"
                    or value == "opera"
                ):
                    webbrowser.register(value, None, webbrowser.BackgroundBrowser)
                if (
                    str(value) != "firefox"
                    and value != "chrome"
                    and value != "safari"
                    and value != "opera"
                    and not "Enable" in value
                ):
                    directory = value
            for log in plotting:
                value = str(list(log.values())[0])
                if "Enable Topic Visualizations" in value:
                    print("Visualizing Topics")
                    self._visualize_topics(model, directory)
                    self.session.logs["info"].append("Visualizing Topics")
                if "Enable Document Visualizations" in value:
                    print("Visualizing Documents")
                    self._visualize_documents(model, directory)
                    self.session.logs["info"].append("Visualizing Documents")
                if "Enable Term Visualizations" in value:
                    print("Visualizing Terms")
                    self._visualize_terms(model, directory)
                    self.session.logs["info"].append("Visualizing Terms")
                if "Enable All Visualizations" in value:
                    print("Visualizing All")
                    self._visualize_topics(model, directory)
                    self._visualize_documents(model, directory)
                    self._visualize_terms(model, directory)
                    self.session.logs["info"].append("Visualizing All")
        else:
            print(
                "No plotting options selected. Visualizing all topics, documents, and terms."
            )
            self._visualize_topics(model, directory)
            self._visualize_documents(model, directory)
            self._visualize_terms(model, directory)
        
            self.session.logs["info"].append("Visualizing All")

    def _visualize_topics(self, model: BERTopic, directory: str = ""):
        try:
            topic_viz = model.visualize_topics()
            if directory != "":
                topic_viz.write_html(f"{directory}/topic_viz.html")
                webbrowser.open_new(file + os.path.realpath(f"{directory}/topic_viz.html"))
            else:
                topic_viz.write_html("topic_viz.html")
                webbrowser.open_new(file + os.path.realpath(f"topic_viz.html"))

        except Exception as e:
            print(e)
            self.session.logs["errors"].append(str(e.with_traceback()))

        try:
            hierarchical_topics = model.hierarchical_topics(docs=self.session.data)
            hierarchical_viz = model.visualize_hierarchy(
                hierarchical_topics=hierarchical_topics
            )

            if directory != "":
                hierarchical_viz.write_html(f"{directory}/hierarchical_viz.html")
                webbrowser.open_new(
                    file + os.path.realpath(f"{directory}/hierarchical_viz.html")
                )
            else:
                hierarchical_viz.write_html("hierarchical_viz.html")
                webbrowser.open_new(file + os.path.realpath("hierarchical_viz.html"))
        except Exception as e:
            print(e)
            self.session.logs["errors"].append(str(e.with_traceback()))
        
        try:
            heatmap = model.visualize_heatmap()

            if directory != "":
                heatmap.write_html(f"{directory}/heatmap.html")
                webbrowser.open_new(
                    file + os.path.realpath(f"{directory}/hierarchical_viz.html")
                )
                webbrowser.open_new(file + os.path.realpath(f"{directory}/heatmap.html"))

            else:
                hierarchical_viz.write_html("hierarchical_viz.html")
                heatmap.write_html("heatmap.html")
                webbrowser.open_new(file + os.path.realpath(f"hierarchical_viz.html"))
                webbrowser.open_new(file + os.path.realpath(f"heatmap.html"))
        except Exception as e:
            print(e)
            self.session.logs["errors"].append(str(e.with_traceback()))

    def _visualize_documents(self, model: BERTopic, directory: str = ""):
        try:
            doc_viz = model.visualize_documents(docs=self.session.data, sample=0.05)

            if directory:
                doc_viz.write_html(f"{directory}/document_viz.html")
                webbrowser.open_new(
                    file + os.path.realpath(f"{directory}/document_viz.html")
                )
            else:
                doc_viz.write_html("document_viz.html")
                webbrowser.open_new(file + os.path.realpath("document_viz.html"))
        except Exception as e:
            print(e)
            self.session.logs["errors"].append(str(e.with_traceback()))

        try:
            hierarchical_topics = model.hierarchical_topics(docs=self.session.data)
            hierarchical_docs = model.visualize_hierarchical_documents(
                docs=self.session.data,
                hierarchical_topics=hierarchical_topics,
                embeddings=model._extract_embeddings(self.session.data),
                nr_levels=math.ceil(math.sqrt(len(hierarchical_topics) // 2)),
                level_scale="log",
            )
    
            if directory:
                hierarchical_docs.write_html(f"{directory}/hierarchical_document_viz.html")
                webbrowser.open_new(
                    file + os.path.realpath(f"{directory}/hierarchical_document_viz.html")
                )
            else:
                hierarchical_docs.write_html("hierarchical_document_viz.html")
                webbrowser.open_new(
                    file + os.path.realpath("hierarchical_document_viz.html")
                )
        except Exception as e:
            print(e)
            self.session.logs["errors"].append(str(e.with_traceback()))
        
    def _visualize_terms(self, model: BERTopic, directory: str = ""):
        try:
            terms = model.visualize_barchart(top_n_topics=50, n_words=10)

            if directory:
                terms.write_html(f"{directory}/term_viz.html")
                webbrowser.open_new(file + os.path.realpath(f"{directory}/term_viz.html"))
            else:
                terms.write_html("term_viz.html")
                webbrowser.open_new(file + os.path.realpath("term_viz.html"))
        except Exception as e:
            print(e)
            self.session.logs["errors"].append(str(e.with_traceback()))


    def _write_logs(self, directory):
        info = self.session.logs["info"]
        errors = self.session.logs["errors"]
        data = self.session.logs["data"]
        logs = {"info": info, "errors": errors, "data": data}
        with open(f"{directory}/logs.json", "w") as f:
            json.dump(logs, f)
        