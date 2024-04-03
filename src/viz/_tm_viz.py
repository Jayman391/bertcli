import pandas as pd
import os
import math
import webbrowser
from bertopic import BERTopic
from src.util._session import Session
from src.viz._ous_viz import HeatMaps
import sys
import shifterator as sh
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
import warnings
import datetime
import traceback

# ignore warnings
warnings.filterwarnings("ignore")
# add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
# configure matplotlib and webbrowser
if sys.platform.startswith("linux"):
    file = ""
else:
    file = "file://"

plt.ioff()

def visualize(model: BERTopic, session: Session, directory: str = "", data: list = []):
    """
    Visualizes the topics, documents, terms, wordshifts, and PDS graphs based on the user's input.

    Args:
        model (BERTopic): The BERTopic model.
        session (Session): The session object.
        directory (str, optional): The directory path. Defaults to "".
        data (list, optional): The list of logs. Defaults to [].

    Returns:
        None
    """
    plotting = [log for log in data if "Plotting" in log.keys()]
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
            if "Enable Document Visualizations" in value:
                print("Visualizing Documents")
                _visualize_documents(model, session, directory)
            if "Enable Term Visualizations" in value:
                print("Visualizing Terms")
                _visualize_terms(model, session, directory)
            if "Enable All Visualizations" in value:
                print("Visualizing All")
                _visualize_topics(model, session, directory)
                _visualize_documents(model, session, directory)
                _visualize_terms(model, session, directory)
            if "Enable Word Shift Graphs" in value:
                _visualize_word_shifts(session, directory)
            if "Enable Power Danger Structure Graphs" in value:
                _visualize_power_danger_structure(session, directory)
    else:
        print(
            "No plotting options selected. Visualizing all topics, documents, and terms,\nas well as word shift and Power-Danger-Structure plots."
        )
        _visualize_topics(model, session, directory)
        _visualize_terms(model, session, directory)
        _visualize_documents(model, session, directory)
        _visualize_word_shifts(session, directory)
        _visualize_power_danger_structure(session, directory)


def _visualize_topics(model: BERTopic, session: Session, directory: str = ""):
    """
    Visualizes the 2d topic map, hierarchical topic tree, and similarity heatmap.

    Args:
        model (BERTopic): The BERTopic model.
        session (Session): The session object.
        directory (str, optional): The directory path. Defaults to "".

    Returns:
        None
    """
    if not os.path.exists(f"{directory}"):
        os.mkdir(f"{directory}")

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
        session.log("errors", {str(datetime.datetime.now()) : traceback.format_exc()})

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
        session.log("errors", {str(datetime.datetime.now()) : traceback.format_exc()})

    try:
        heatmap = model.visualize_heatmap()

        if directory != "":
            heatmap.write_html(f"{directory}/heatmap.html")
            webbrowser.open_new(file + os.path.realpath(f"{directory}/heatmap.html"))
        else:
            heatmap.write_html("heatmap.html")
            webbrowser.open_new(file + os.path.realpath(f"heatmap.html"))
    except Exception as e:
        print(e)
        session.log("errors", {str(datetime.datetime.now()) : traceback.format_exc()})


def _visualize_documents(model: BERTopic, session: Session, directory: str = ""):
    """
    Visualizes the documents in 2d and hierarchical document tree in 2d.

    Args:
        model (BERTopic): The BERTopic model.
        session (Session): The session object.
        directory (str, optional): The directory path. Defaults to "".

    Returns:
        None
    """
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
        session.log("errors", {str(datetime.datetime.now()) : traceback.format_exc()})

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
        session.log("errors", {str(datetime.datetime.now()) : traceback.format_exc()})


def _visualize_terms(model: BERTopic, session: Session, directory: str = ""):
    try:
        terms = model.visualize_barchart(top_n_topics=500, n_words=10)

        if directory:
            terms.write_html(f"{directory}/term_viz.html")
            webbrowser.open_new(file + os.path.realpath(f"{directory}/term_viz.html"))
        else:
            terms.write_html("term_viz.html")
            webbrowser.open_new(file + os.path.realpath("term_viz.html"))
    except Exception as e:
        print(e)
        session.log("errors", {str(datetime.datetime.now()) : traceback.format_exc()})


def _visualize_word_shifts(session: Session, directory: str = ""):
    """
    Visualizes word shifts between topics and samples.

    Args:
        session (Session): The session object.
        directory (str, optional): The directory path. Defaults to "".

    Raises:
        ValueError: If the number of topics is not equal to the number of samples.

    Returns:
        None
    """
    try:
        # in directory, there is a sub directory named topics. For each topic, there is a file named topic_zipf.csv
        # and topic_sample_zipf.csv.
        # get all files in directory/topics
        files = os.listdir(f"{directory}/topics")

        samples = [f for f in files if "sample" in f]
        files = [f for f in files if "sample" not in f]

        labmt = pd.read_csv("src/viz/LABMT.csv")

        # calculate sentiment of corpus

        lens_min = 4
        lens_max = 6

        for i, file in enumerate(files):

            topic_words = pd.read_csv(f"{directory}/topics/{file}")
            sample_words = pd.read_csv(f"{directory}/topics/{samples[i]}")

            # turn the types and counts columns into dicts
            topic_words = dict(zip(topic_words["types"], topic_words["counts"]))

            sample_words = dict(zip(sample_words["types"], sample_words["counts"]))

            # filter through lens
            topic_words = {
                k: v
                for k, v in topic_words.items()
                if k in labmt["Word"].values
                and (
                    labmt[labmt["Word"] == k]["Happiness Score"].values[0] < lens_min
                    or labmt[labmt["Word"] == k]["Happiness Score"].values[0] > lens_max
                )
            }

            sample_words = {
                k: v
                for k, v in sample_words.items()
                if k in labmt["Word"].values
                and (
                    labmt[labmt["Word"] == k]["Happiness Score"].values[0] < lens_min
                    or labmt[labmt["Word"] == k]["Happiness Score"].values[0] > lens_max
                )
            }

            sample_total_counts = sum(sample_words.values())

            if sample_total_counts:

                sample_sentiment = {
                    k: v
                    / sample_total_counts
                    * labmt[labmt["Word"] == k]["Happiness Score"].values[0]
                    for k, v in sample_words.items()
                }
                sample_full_sentiment = sum(sample_sentiment.values())

                shift_graph = sh.WeightedAvgShift(
                    type2freq_1=sample_words,
                    type2freq_2=topic_words,
                    type2score_1="labMT_English",
                    type2score_2="labMT_English",
                    reference_value=sample_full_sentiment,
                    handle_missing_scores="exclude",
                )

                plt.figure(figsize=(10, 10))

                g = shift_graph.get_shift_graph(show_plot=False)

                plt.savefig(
                    f"{directory}/topics/{file.split(sep='.')[0]}_wordshift.png"
                )

                plt.close()

    except Exception as e:
        print(e)
        session.log("errors", {str(datetime.datetime.now()) : traceback.format_exc()})


def _safe_read_csv(file_path, session):
    try:
        return pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError as e:
        print(e)
        session.log("errors", {str(datetime.datetime.now()) : traceback.format_exc()})
        return None


def _process_dataframe_for_visualization(df: pd.DataFrame, ous, session):
    """
    performs SVD on the df after being filtered through the VAD dataframe and constructs the resulting PDS dimesions.
    """
    try:
        df = df[df["types"].isin(ous["word"])]
        df = df.drop_duplicates(subset=["types"])
        df["total_unique"] = len(df)
        df_copy = df.copy()
        df = df.merge(ous, left_on="types", right_on="word")
        df.drop(
            columns=["counts", "types", "word", "probs", "total_unique"], inplace=True
        )
        df = df.apply(pd.to_numeric)

        df = df.dropna(axis=1)

        if df.shape[1] < 3:
            return None, None

        svd = TruncatedSVD(n_components=3)
        components = svd.fit_transform(df)

        df_transformed = pd.DataFrame(
            components, columns=["Power", "Danger", "Structure"]
        )

        # Apply the rotation if necessary
        df_transformed["Power"] = df_transformed["Power"] * math.pi / 4
        df_transformed["Danger"] = df_transformed["Danger"] * math.pi / 4

        return df_transformed, df_copy
    except Exception as e:
        print(e)
        session.log("errors", {str(datetime.datetime.now()) : traceback.format_exc()})
        return None, None


def _visualize_heatmap_from_df(df, xcol, ycol, directory, file_base_name, session):
    """
    Visualizes a heatmap from a DataFrame. Uses code written by 
    The Computational Story Lab at the University of Vermont.

    Args:
        df (pd.DataFrame): The DataFrame to visualize.
        xcol (str): The column to use for the x-axis.
        ycol (str): The column to use for the y-axis.
        directory (str): The directory to save the visualization.
        file_base_name (str): The base name for the file.

    Returns:
        None 
    """
    try:
        # Create a new figure explicitly to ensure it's fresh
        fig, ax = plt.subplots()  # This creates a new figure and axes for the plot

        # Assuming HeatMaps.generate_heatmap_from_df exists and works correctly.
        # We need to pass the `ax` argument to use the newly created axes.
        im = HeatMaps.generate_heatmap_from_df(df, xcol, ycol, ax=ax)

        plt.xlabel(xcol)
        plt.ylabel(ycol)
        plt.savefig(f"{directory}/topics/{file_base_name}_{xcol}_{ycol}.png")

        plt.close(fig)  # Close the figure to free up memory
    except Exception as e:
        print(e)
        session.log("errors", {str(datetime.datetime.now()) : traceback.format_exc()})


def _visualize_power_danger_structure(session, directory):
    """"
    Performs PDS calculations for every cluster and visualizes the results as heatmaps.

    Args:
        directory (str): The directory to save the visualizations.

    Returns:
        None
    """
   
    ous = pd.read_csv("src/viz/NRC-VAD.txt", delimiter=" ")
    if ous is None:
        return

    for file in os.listdir(f"{directory}/topics"):
        if file.endswith(".csv") and "sample" not in file:
            df = _safe_read_csv(os.path.join(f"{directory}/topics", file), session)
            if df is not None:
                df_transformed, df = _process_dataframe_for_visualization(df, ous, session)
                if df_transformed is not None:
                    file_base_name = os.path.splitext(file)[0]
                    try :
                        _visualize_heatmap_from_df(
                            df_transformed, "Power", "Danger", directory, file_base_name, session
                        )

                        _visualize_heatmap_from_df(
                            df_transformed, "Power", "Structure", directory, file_base_name, session
                        )

                        _visualize_heatmap_from_df(
                            df_transformed, "Danger", "Structure", directory, file_base_name, session
                        )
                    except Exception as e:
                        print(e)
                        session.log("errors", {str(datetime.datetime.now()) : traceback.format_exc()})
                        
                    try : 

                        df = pd.merge(df, df_transformed, left_index=True, right_index=True)

                        df.to_csv(
                            f"{directory}/topics/{file_base_name}_transformed.csv",
                            index=False,
                        )
                    
                    except Exception as e:
                        print(e)
                        session.log("errors", {str(datetime.datetime.now()) : traceback.format_exc()})
                      