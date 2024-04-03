import pytest
import numpy as np
import pandas as pd
from collections import defaultdict
from util._formatter import DataFormatter

@pytest.fixture
def formatter():
    return DataFormatter()

def test_convert_content_to_iso_format(formatter):
    content = np.array([{"date": "2022-01-01"}, {"date": "2022-02-02"}])
    expected_result = np.array([{"date": "2022-01-01T00:00:00"}, {"date": "2022-02-02T00:00:00"}])
    formatter.convert_content_to_iso_format(content)
    assert np.array_equal(content, expected_result)

def test_format_text_data(formatter):
    posts = ["This is a post.", "Another post."]
    comments = ["Nice post!", "Great job!"]
    expected_result = {"this": 1, "is": 1, "a": 1, "post": 3, "another": 1, "nice": 1, "great": 1, "job": 1}
    result = formatter.format_text_data(posts, comments)
    assert result == expected_result

def test_sort_data(formatter):
    data = {"this": 1, "is": 2, "a": 3}
    expected_result = [("a", 3), ("is", 2), ("this", 1)]
    result = formatter.sort_data(data)
    assert result == expected_result

def test_compute_zipf(formatter):
    sorted_data = [("a", 3), ("is", 2), ("this", 1)]
    expected_result = np.array([
        ("a", 3, 0.5, 3),
        ("is", 2, 0.3333333333333333, 3),
        ("this", 1, 0.16666666666666666, 3)
    ], dtype=formatter.dtypes)
    result = formatter.compute_zipf(sorted_data)
    assert np.array_equal(result, expected_result)

def test_text_data_to_zipf(formatter):
    posts = ["This is a post.", "Another post."]
    comments = ["Nice post!", "Great job!"]
    expected_result = np.array([
        ("post", 3, 0.3, 8),
        ("this", 1, 0.1, 8),
        ("is", 1, 0.1, 8),
        ("a", 1, 0.1, 8),
        ("another", 1, 0.1, 8),
        ("nice", 1, 0.1, 8),
        ("great", 1, 0.1, 8),
        ("job", 1, 0.1, 8)
    ], dtype=formatter.dtypes)
    result = formatter.text_data_to_zipf(posts, comments)
    assert np.array_equal(result, expected_result)

def test_zipf_data_to_dataframe(formatter):
    posts = ["This is a post.", "Another post."]
    comments = ["Nice post!", "Great job!"]
    expected_result = pd.DataFrame({
        "types": ["post", "this", "is", "a", "another", "nice", "great", "job"],
        "counts": [3, 1, 1, 1, 1, 1, 1, 1],
        "probs": [0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
        "total_unique": [8, 8, 8, 8, 8, 8, 8, 8]
    })
    result = formatter.zipf_data_to_dataframe(posts, comments)
    assert result.equals(expected_result)

def test_zipf_data_to_json(formatter):
    posts = ["This is a post.", "Another post."]
    comments = ["Nice post!", "Great job!"]
    expected_result = {
        0: {"types": "post", "counts": 3, "probs": 0.3, "total_unique": 8},
        1: {"types": "this", "counts": 1, "probs": 0.1, "total_unique": 8},
        2: {"types": "is", "counts": 1, "probs": 0.1, "total_unique": 8},
        3: {"types": "a", "counts": 1, "probs": 0.1, "total_unique": 8},
        4: {"types": "another", "counts": 1, "probs": 0.1, "total_unique": 8},
        5: {"types": "nice", "counts": 1, "probs": 0.1, "total_unique": 8},
        6: {"types": "great", "counts": 1, "probs": 0.1, "total_unique": 8},
        7: {"types": "job", "counts": 1, "probs": 0.1, "total_unique": 8}
    }
    result = formatter.zipf_data_to_json(posts, comments)
    assert result == expected_result