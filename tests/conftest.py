# conftest.py
import pytest
import pandas as pd
import sys
import os

# Add the source directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


# Define the sample_data fixture
@pytest.fixture
def sample_data():
    # Create a sample DataFrame for testing
    data = pd.DataFrame(
        {
            "text": [
                "This is the first document.",
                "This document is the second document.",
                "And this is the third one.",
                "Is this the first document?",
            ]
        }
    )
    return data
