from bertopic import BERTopic
import os
import pandas as pd
from util._session import Session
from drivers._tm_driver import TopicDriver
from util._formatter import DataFormatter
from viz._tm_viz import visualize, _visualize_topics, _visualize_documents, _visualize_terms,_visualize_word_shifts, _visualize_heatmap_from_df, _visualize_power_danger_structure, _process_dataframe_for_visualization, _safe_read_csv

session = Session()

model = BERTopic()

data = _safe_read_csv(file_path="tests/test_data/usa-vaccine-comments.csv", session=session)

docs = data["text"].tolist()[:1000]

session.set_data(docs)

topics, _ = model.fit_transform(docs)

os.makedirs("output", exist_ok=True)


def test_visualize_topics():
    _visualize_topics(model, session, 'output')
    assert os.path.exists("output/topic_viz.html")
    assert os.path.exists("output/hierarchical_viz.html")
    assert os.path.exists("output/heatmap.html")

def test_visualize_documents():
    _visualize_documents(model, session, 'output')
    assert os.path.exists("output/document_viz.html")
    assert os.path.exists("output/hierarchical_document_viz.html")

def test_visualize_terms():
    _visualize_terms(model, session, 'output')
    assert os.path.exists("output/term_viz.html")

def test_visualize_word_shifts():
    driver = TopicDriver()
    formatter = DataFormatter() 
    session_data = pd.DataFrame(list(zip(session.data, topics)), columns=["text", "label"])
    driver._save_zipf_distribution(session_data, 'output', formatter)

    _visualize_word_shifts(session, 'output')

    assert os.path.exists("output/topics/0_zipf_wordshift.png")
