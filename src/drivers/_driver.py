from abc import ABC
from src.menus._menu import Menu
from src.loading._dataloader import DataLoader
from util._session import Session
import webbrowser
from webbrowser import open_new_tab
from bertopic import BERTopic
import os
import math


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
        topics, _ = model.fit_transform(self.session.data)
        # set -1 cluster to num_clusters+1
        num_topics = len(set(topics))

        topics = [
            topic if topic != -1 and isinstance(topic, bool) == False else num_topics
            for topic in topics
        ]
        self.session.logs["info"].append("Topics have been extracted")
        data = self.session.logs["data"]
        #remove all logs that containg Back in the values
        data = [log for log in data if "Back" not in log.values()]
        plotting = [log for log in data if "Plotting" in log.keys()]
        dir = ""
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
                    dir = value
            for log in plotting:
                value = str(list(log.values())[0])
                if "Enable Topic Visualizations" in value:
                    print("Visualizing Topics")
                    self._visualize_topics(model, dir)
                    self.session.logs["info"].append("Visualizing Topics")
                if "Enable Document Visualizations" in value:
                    print("Visualizing Documents")
                    self._visualize_documents(model, dir)
                    self.session.logs["info"].append("Visualizing Documents")
                if "Enable Term Visualizations" in value:
                    print("Visualizing Terms")
                    self._visualize_terms(model, dir)
                    self.session.logs["info"].append("Visualizing Terms")
                if "Enable All Visualizations" in value:
                    print("Visualizing All")
                    self._visualize_topics(model, dir)
                    self._visualize_documents(model, dir)
                    self._visualize_terms(model, dir)
                    self.session.logs["info"].append("Visualizing All")
        else:
            print(
                "No plotting options selected. Visualizing all topics, documents, and terms."
            )
            self._visualize_topics(model, dir)
            self._visualize_documents(model, dir)
            self._visualize_terms(model, dir)
        
            self.session.logs["info"].append("Visualizing All")

    def _visualize_topics(self, model: BERTopic, dir: str = ""):
        try:
            topic_viz = model.visualize_topics()
            if dir != "":
                topic_viz.write_html(f"{dir}/topic_viz.html")
                webbrowser.open_new("file://" + os.path.realpath(f"{dir}/topic_viz.html"))
            else:
                topic_viz.write_html("topic_viz.html")
                webbrowser.open_new("file://" + os.path.realpath(f"topic_viz.html"))

        except Exception as e:
            print(e)
            self.session.logs["errors"].append(str(e.with_traceback()))

        try:
            hierarchical_topics = model.hierarchical_topics(docs=self.session.data)
            hierarchical_viz = model.visualize_hierarchy(
                hierarchical_topics=hierarchical_topics
            )

            if dir != "":
                hierarchical_viz.write_html(f"{dir}/hierarchical_viz.html")
                webbrowser.open_new(
                    "file://" + os.path.realpath(f"{dir}/hierarchical_viz.html")
                )
            else:
                hierarchical_viz.write_html("hierarchical_viz.html")
                webbrowser.open_new("file://" + os.path.realpath("hierarchical_viz.html"))
        except Exception as e:
            print(e)
            self.session.logs["errors"].append(str(e.with_traceback()))
        
        try:
            heatmap = model.visualize_heatmap()

            if dir != "":
                heatmap.write_html(f"{dir}/heatmap.html")
                webbrowser.open_new(
                    "file://" + os.path.realpath(f"{dir}/hierarchical_viz.html")
                )
                webbrowser.open_new("file://" + os.path.realpath(f"{dir}/heatmap.html"))

            else:
                hierarchical_viz.write_html("hierarchical_viz.html")
                heatmap.write_html("heatmap.html")
                webbrowser.open_new("file://" + os.path.realpath(f"hierarchical_viz.html"))
                webbrowser.open_new("file://" + os.path.realpath(f"heatmap.html"))
        except Exception as e:
            print(e)
            self.session.logs["errors"].append(str(e.with_traceback()))

    def _visualize_documents(self, model: BERTopic, dir: str = ""):
        try:
            doc_viz = model.visualize_documents(docs=self.session.data, sample=0.05)

            if dir:
                doc_viz.write_html(f"{dir}/document_viz.html")
                webbrowser.open_new(
                    "file://" + os.path.realpath(f"{dir}/document_viz.html")
                )
            else:
                doc_viz.write_html("document_viz.html")
                webbrowser.open_new("file://" + os.path.realpath("document_viz.html"))
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

            if dir:
                hierarchical_docs.write_html(f"{dir}/hierarchical_document_viz.html")
                webbrowser.open_new(
                    "file://" + os.path.realpath(f"{dir}/hierarchical_document_viz.html")
                )
            else:
                hierarchical_docs.write_html("hierarchical_document_viz.html")
                webbrowser.open_new(
                    "file://" + os.path.realpath("hierarchical_document_viz.html")
                )
        except Exception as e:
            print(e)
            self.session.logs["errors"].append(str(e.with_traceback()))
        
    def _visualize_terms(self, model: BERTopic, dir: str = ""):
        try:
            terms = model.visualize_barchart(top_n_topics=50, n_words=10)

            if dir:
                terms.write_html(f"{dir}/term_viz.html")
                webbrowser.open_new("file://" + os.path.realpath(f"{dir}/term_viz.html"))
            else:
                terms.write_html("term_viz.html")
                webbrowser.open_new("file://" + os.path.realpath("term_viz.html"))
        except Exception as e:
            print(e)
            self.session.logs["errors"].append(str(e.with_traceback()))
