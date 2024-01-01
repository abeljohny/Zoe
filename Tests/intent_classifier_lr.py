from os import fsdecode, listdir, path
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split


class IntentClassifierLR(object):
    TRAININGSET_DIR = "assets/intent_sets"

    def __init__(self):
        """Initialize Intent Classifier"""
        self._corpus, self._labels = [], []
        self._clf, self._vectorizer = None, None
        self._load_trainingset()

    def _load_trainingset(self) -> None:
        """Load training set and labels (filenames) into memory for training the classifier"""
        directory_path = IntentClassifierLR.TRAININGSET_DIR
        for dataset_name in listdir(directory_path):
            with open(
                file=path.join(directory_path, fsdecode(dataset_name)),
                mode="r",
                encoding="utf-8",
            ) as dataset:
                intent = Path(dataset_name).stem
                split_data = dataset.read().splitlines()
                self._labels += [intent] * len(split_data)
                self._corpus += split_data

    def evaluate(self):
        """Split training set into training and test sets and vectorize them"""
        (
            data_train,
            data_test,
            y_train,
            y_test,
        ) = train_test_split(
            self._corpus,
            self._labels,
            stratify=self._labels,
            test_size=0.25,
            random_state=42,
        )
        self._vectorizer = TfidfVectorizer(
            sublinear_tf=True,
        )
        data_train_vec = self._vectorizer.fit_transform(data_train)
        data_test_vec = self._vectorizer.transform(data_test)
        self._clf = LogisticRegression()
        self._clf.fit(data_train_vec, y_train)
        y_pred = self._clf.predict(data_test_vec)

        print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
        print(f"Confusion Matrix:\n {confusion_matrix(y_test, y_pred)}")
        print(f"Classification Report: {classification_report(y_test, y_pred)}")
