from abc import ABC, abstractmethod


class IntentABC(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def handle(self, request, intent) -> str:
        pass

    @abstractmethod
    def continue_conversation(self, request, intent) -> str:
        pass
