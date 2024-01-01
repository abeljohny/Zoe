from Tests.intent_classifier_lr import IntentClassifierLR
from config import config
from intent_classifier import IntentClassifier


def intent_classifier_svc_metrics():
    clf = IntentClassifier(config())
    clf.evaluate()


def intent_classifier_lr_metrics():
    clf = IntentClassifierLR(config())
    clf.evaluate()
