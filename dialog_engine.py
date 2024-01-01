from config import Config
from constants import Intent, Reprompts
from intent_classifier import IntentClassifier
from intent_handlers.book import Book
from intent_handlers.cancel import Cancel
from intent_handlers.introspect import Introspect
from intent_handlers.qa import QA


class DialogEngine(object):
    ACCEPTED_CONFIDENCE_THRESHOLD = 0.5

    def __init__(self, config: Config, user, memory):
        self._config = config
        self._user = user
        self._memory = memory
        self._intent_clf = IntentClassifier(self._config)

    def form_reply(self, query):
        recent_dialog_state = self._memory.read_recent_dialog_state()

        # continue multi-turn interaction
        if recent_dialog_state:
            match recent_dialog_state["intent"]:
                case Intent.NAMEOPS.value:
                    return QA(
                        self._config, self._memory, self._user
                    ).continue_conversation(query, Intent.NAMEOPS.value)
                case Intent.BOOK.value:
                    return Book(
                        self._config, self._memory, self._user
                    ).continue_conversation(query, Intent.BOOK.value)
                case Intent.INTROSPECT.value:
                    return Introspect(
                        self._config, self._memory, self._user
                    ).continue_conversation(query, Intent.INTROSPECT.value)
                case Intent.CANCEL.value:
                    return Cancel(
                        self._config, self._memory, self._user
                    ).continue_conversation(query, Intent.CANCEL.value)

        # intent classification and routing
        intent, confidence = self._intent_clf.predict(query)
        if confidence[0][1] < self._config.CONFIDENCE_THRESHOLD:
            intent = ""
        match intent:
            case Intent.GREETING.value | Intent.SMALLTALK.value | Intent.NAMEOPS.value:
                return QA(self._config, self._memory, self._user).handle(query, intent)
            case Intent.BOOK.value:
                return Book(self._config, self._memory, self._user).handle(
                    query, intent
                )
            case Intent.INTROSPECT.value:
                return Introspect(self._config, self._memory, self._user).handle(
                    query, intent
                )
            case Intent.CANCEL.value:
                return Cancel(self._config, self._memory, self._user).handle(
                    query, intent
                )
            case _:
                return Reprompts.REPHRASE.value
