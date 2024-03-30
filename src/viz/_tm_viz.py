import os
import math
import webbrowser
from webbrowser import open_new_tab
from bertopic import BERTopic
from src.util._session import Session
import sys

if sys.platform.startswith("linux"):
    file = ""
else:
    file = "file://"

def visualize(model: BERTopic, session:Session , directory: str = "", data: list = []):
        plotting = [log for log in data if "Plotting" in log.keys()]
        session.logs["info"].append("Plotting Topics")
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
                    _visualize_topics(model, session, directory)
                    session.logs["info"].append("Visualizing Topics")
                if "Enable Document Visualizations" in value:
                    print("Visualizing Documents")
                    _visualize_documents(model, session, directory)
                    session.logs["info"].append("Visualizing Documents")
                if "Enable Term Visualizations" in value:
                    print("Visualizing Terms")
                    _visualize_terms(model, session, directory)
                    session.logs["info"].append("Visualizing Terms")
                if "Enable All Visualizations" in value:
                    print("Visualizing All")
                    _visualize_topics(model, session, directory)
                    _visualize_documents(model, session, directory)
                    _visualize_terms(model, session, directory)
                    session.logs["info"].append("Visualizing All")
        else:
            print(
                "No plotting options selected. Visualizing all topics, documents, and terms by default."
            )
            _visualize_topics(model, session, directory)
            _visualize_documents(model, session, directory)
            _visualize_terms(model, session, directory)

            session.logs["info"].append("Visualizing All")

def _visualize_topics(model: BERTopic, session:Session , directory: str = ""):
    try:
        topic_viz = model.visualize_topics()
        if directory != "":
            topic_viz.write_html(f"{directory}/topic_viz.html")
            webbrowser.open_new(
                file + os.path.realpath(f"{directory}/topic_viz.html")
            )
        else:
            topic_viz.write_html("topic_viz.html")
            webbrowser.open_new(file + os.path.realpath(f"topic_viz.html"))

    except Exception as e:
        print(e)
        session.logs["errors"].append(str(e.with_traceback()))

    try:
        hierarchical_topics = model.hierarchical_topics(docs=session.data)
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
        session.logs["errors"].append(str(e.with_traceback()))

    try:
        heatmap = model.visualize_heatmap()

        if directory != "":
            heatmap.write_html(f"{directory}/heatmap.html")
            webbrowser.open_new(
                file + os.path.realpath(f"{directory}/heatmap.html")
            )
        else:
            heatmap.write_html("heatmap.html")
            webbrowser.open_new(file + os.path.realpath(f"heatmap.html"))
    except Exception as e:
        print(e)
        session.logs["errors"].append(str(e.with_traceback()))

def _visualize_documents( model: BERTopic, session:Session , directory: str = ""):
    try:
        doc_viz = model.visualize_documents(docs=session.data, sample=0.05)

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
        session.logs["errors"].append(str(e.with_traceback()))

    try:
        hierarchical_topics = model.hierarchical_topics(docs=session.data)
        hierarchical_docs = model.visualize_hierarchical_documents(
            docs=session.data,
            hierarchical_topics=hierarchical_topics,
            embeddings=model._extract_embeddings(session.data),
            nr_levels=math.ceil(math.sqrt(len(hierarchical_topics) // 2)),
            level_scale="log",
        )

        if directory:
            hierarchical_docs.write_html(
                f"{directory}/hierarchical_document_viz.html"
            )
            webbrowser.open_new(
                file
                + os.path.realpath(f"{directory}/hierarchical_document_viz.html")
            )
        else:
            hierarchical_docs.write_html("hierarchical_document_viz.html")
            webbrowser.open_new(
                file + os.path.realpath("hierarchical_document_viz.html")
            )
    except Exception as e:
        print(e)
        session.logs["errors"].append(str(e.with_traceback()))

def _visualize_terms( model: BERTopic, session:Session , directory: str = ""):
    try:
        terms = model.visualize_barchart(top_n_topics=500, n_words=10)

        if directory:
            terms.write_html(f"{directory}/term_viz.html")
            webbrowser.open_new(
                file + os.path.realpath(f"{directory}/term_viz.html")
            )
        else:
            terms.write_html("term_viz.html")
            webbrowser.open_new(file + os.path.realpath("term_viz.html"))
    except Exception as e:
        print(e)
        session.logs["errors"].append(str(e.with_traceback()))