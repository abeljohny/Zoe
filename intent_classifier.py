import operator
from os import fsdecode, listdir, path
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.svm import SVC

from config import Config
from file_manager import FileManager


class IntentClassifier(object):
    CLASSIFIER_FILEPATH = "assets/pickles/models/intent_classifier.pkl"
    VECTORIZER_FILEPATH = "assets/pickles/models/tfidf_vectorizer.pkl"
    TRAININGSET_DIR = "assets/intent_sets"

    def __init__(self, config: Config):
        """Initialize Intent Classifier

        :param config: configuration object providing configuration details for the session
        """
        self._config = config
        self._clf = FileManager.load_pickle(
            self.CLASSIFIER_FILEPATH, quiet=self._config.quiet
        )
        self._vectorizer = FileManager.load_pickle(
            self.VECTORIZER_FILEPATH, quiet=self._config.quiet
        )
        if (
            self._clf is None
            or self._vectorizer is None
            or self._config.reindex is True
        ):
            self._corpus, self._labels = [], []
            self._clf, self._vectorizer = self.train()
            FileManager.save_pickle(
                self._clf, self.CLASSIFIER_FILEPATH, self._config.quiet
            )
            FileManager.save_pickle(
                self._vectorizer, self.VECTORIZER_FILEPATH, self._config.quiet
            )

    def predict(self, text: str):
        """Predict intent of a given text

        :param text: text to be classified
        :return: predicted intent and N-best list of classes with corresponding confidence score
        """
        vectorized_text = self._vectorizer.transform([text])

        # create N-best list
        class_confidence = {}
        confidences = self._clf.predict_proba(vectorized_text)
        for idx, cls in enumerate(self._clf.classes_):
            class_confidence[cls] = confidences[0][idx]

        return self._clf.predict(vectorized_text)[0], sorted(
            class_confidence.items(), key=operator.itemgetter(1), reverse=True
        )

    def _load_trainingset(self) -> None:
        """Load training set and labels (filenames) into memory for training the classifier"""
        directory_path = IntentClassifier.TRAININGSET_DIR
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
        data_train_vec = self._vectorizer.fit_transform(data_train)
        data_test_vec = self._vectorizer.transform(data_test)
        self._clf = SVC(kernel="linear", probability=True)
        self._clf.fit(data_train_vec, y_train)
        y_pred = self._clf.predict(data_test_vec)

        print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
        print(f"Confusion Matrix:\n {confusion_matrix(y_test, y_pred)}")
        print(f"Classification Report: {classification_report(y_test, y_pred)}")

        kfold = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
        return cross_val_score(
            self._clf, self._corpus, self._labels, cv=kfold, scoring="accuracy"
        )

    def train(self):
        """Trains a classifier to classify intents using Support Vector Classification"""
        self._load_trainingset()
        vectorizer = TfidfVectorizer(
            sublinear_tf=True,
        )
        X_train = vectorizer.fit_transform(self._corpus)
        return (
            SVC(kernel="linear", probability=True).fit(X_train, self._labels),
            vectorizer,
        )
