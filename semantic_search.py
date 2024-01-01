import csv

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import Config
from util import Util


class SemanticSearch(object):
    REPLYSET_FILEPATH = "assets/reply_set.csv"

    def __init__(self, config: Config):
        """Initialize Search

        :param config: configuration object providing configuration details for the session
        """
        self._config = config
        self._vectorizer = CountVectorizer()
        self._corpus = []
        self._replies = {}

        self._load_corpus()

    def _load_corpus(self) -> None:
        """Load reply set for question answering"""
        with open(self.REPLYSET_FILEPATH, "r") as reply:
            reader = csv.DictReader(reply)
            for row in reader:
                self._corpus.append(Util.rm_special_chars(row["Question"]))
                self._replies[row["Key"]] = row["Answer"]

        self._corpus = self._vectorizer.fit_transform(self._corpus)

    def _similar(self, query):
        query_vector = self._vectorizer.transform([query])
        similarity_matrix = cosine_similarity(query_vector, self._corpus)[0]
        return (
            similarity_matrix.max(),
            self._replies[str(similarity_matrix.argsort()[-1] + 1)],
        )

    def search(self, query: str):
        """Returns the reply having the highest cosine similarity with query

        :param query: query to be searched
        :return: response having the highest cosine similarity with query
        """
        _, reply = self._similar(query)
        return reply
