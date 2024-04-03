from collections import defaultdict
import numpy as np
import pandas as pd
import re


class DataFormatter:
    """
    A class that provides methods for formatting and analyzing data.
    """

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
        """
        Converts the date field in the content array to ISO format.

        Args:
            content (np.array): The array containing the content data.

        Returns:
            np.array: The modified content array with the date field converted to ISO format.
        """
        for content_dict in content:
            content_dict[self.DATE_FIELD] = pd.to_datetime(content_dict[self.DATE_FIELD]).isoformat()

    def format_text_data(self, posts: list, comments: list = None):
        """
        Formats the text data by cleaning, tokenizing, and calculating word frequency.

        Args:
            posts (list): A list of posts.
            comments (list, optional): A list of comments. Defaults to None.

        Returns:
            dict: A dictionary containing the word frequency of the text data.
        """
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
        """
        Sorts the data in descending order based on the values.

        Args:
            data (dict): The data to be sorted.

        Returns:
            list: A list of tuples containing the sorted data.
        """
        return sorted(data.items(), key=lambda x: x[1], reverse=True)

    def compute_zipf(self, sorted_data):
        """
        Computes the Zipfian distrubition for the sorted data.

        Args:
            sorted_data (list): The sorted data.

        Returns:
            np.array: An array containing Zipfian distrubition statistics.
        """
        total = np.sum(val for _, val in sorted_data)
        return np.array(
            [(item, val, (val / total), len(sorted_data)) for item, val in sorted_data],
            dtype=self.dtypes,
        )

    def text_data_to_zipf(self, posts, comments=None):
        """
        Converts the text data to Zipfian distrubition.

        Args:
            posts (list): A list of posts.
            comments (list, optional): A list of comments. Defaults to None.

        Returns:
            np.array: An array containing the Zipfian distrubition for the text data.
        """
        word_freq = self.format_text_data(posts, comments)
        sorted_word_freq = self.sort_data(word_freq)
        self.word_freq_zipf = self.compute_zipf(sorted_word_freq)
        return self.word_freq_zipf

    def zipf_data_to_dataframe(self, posts, comments=None):
        """
        Converts the Zipfian distrubition to a pandas DataFrame.

        Args:
            posts (list): A list of posts.
            comments (list, optional): A list of comments. Defaults to None.

        Returns:
            pd.DataFrame: A DataFrame containing the Zipfian distrubition.
        """
        self.word_freq_zipf = self.text_data_to_zipf(posts, comments)
        return pd.DataFrame(self.word_freq_zipf)

    def zipf_data_to_json(self, posts, comments=None):
        """
        Converts the Zipfian distrubition to a JSON object.

        Args:
            posts (list): A list of posts.
            comments (list, optional): A list of comments. Defaults to None.

        Returns:
            dict: A dictionary containing the Zipfian distrubition.
        """
        zipf = self.text_data_to_zipf(posts, comments)
        return pd.DataFrame(zipf).to_dict(orient="index")
