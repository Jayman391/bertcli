from collections import defaultdict
import numpy as np
import pandas as pd
import re


class DataFormatter:
    dtypes = [
        ("types", object),
        ("counts", int),
        ("probs", float),
        ("total_unique", int),
    ]

    DATE_FIELD = "date"

    def __init__(self):
        self.word_freq_zipf = np.empty(0, dtype=self.dtypes)
        self.group_size_zipf = np.empty(0, dtype=self.dtypes)

    def convert_content_to_iso_format(self, content: np.array) -> np.array:
        for content_dict in content:
            content_dict[self.DATE_FIELD] = content_dict[self.DATE_FIELD].isoformat()

    def format_text_data(self, posts: list, comments: list = None):

        if comments is not None:
            corpus = posts + comments
        else:
            corpus = posts

        # Calculate word frequency
        word_freq = defaultdict(int)
        total_words = []
        for text in corpus:
            # Replace \n and \t with space
            cleaned_text = re.sub(r"[\n\t]", " ", text.lower())
            # Remove punctuation
            cleaned_text = re.sub(r"[^\w\s]", "", cleaned_text)
            # split into words
            words = cleaned_text.split(" ")
            total_words += words
        for word in total_words:
            if word != "":
                word_freq[word] += 1
        return dict(word_freq)

    def sort_data(self, data):
        # Sort the data in descending order
        return sorted(data.items(), key=lambda x: x[1], reverse=True)

    def compute_zipf(self, sorted_data):
        total = np.sum(val for _, val in sorted_data)
        return np.array(
            [(item, val, (val / total), len(sorted_data)) for item, val in sorted_data],
            dtype=self.dtypes,
        )

    def text_data_to_zipf(self, posts, comments=None):
        word_freq = self.format_text_data(posts, comments)
        sorted_word_freq = self.sort_data(word_freq)
        self.word_freq_zipf = self.compute_zipf(sorted_word_freq)
        return self.word_freq_zipf

    def zipf_data_to_dataframe(self, posts, comments=None):
        self.word_freq_zipf = self.text_data_to_zipf(posts, comments)
        return pd.DataFrame(self.word_freq_zipf)

    def zipf_data_to_json(self, posts, comments=None):
        zipf = self.text_data_to_zipf(posts, comments)
        return pd.DataFrame(zipf).to_dict(orient="index")
