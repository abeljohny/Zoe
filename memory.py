from collections import deque

from calendar import Calendar


class Memory(object):
    def __init__(self, config) -> None:
        self._botname = "Zoe"
        self._dialog_state_cache = deque()
        self._config = config
        self._calendar = Calendar(self._config)

    @property
    def botname(self):
        return self._botname

    @property
    def calendar(self):
        return self._calendar

    def update_botname(self, botname):
        self._botname = botname
        return self._botname

    @staticmethod
    def initialize_dialog_state(
        intent=None,
        date=None,
        time_start=None,
        time_end=None,
        appointmment=None,
        name=None,
        tag=None,
    ):
        return {
            "intent": intent,
            "data": {
                "date": date,
                "time_start": time_start,
                "time_end": time_end,
                "appointment": appointmment,
                "name": name,
                "tag": tag,
            },
        }

    def enqueue_dialog_state(self, dialog_state):
        self._dialog_state_cache.append(dialog_state)
        return self._dialog_state_cache

    def dequeue_dialog_state(self):
        return self._dialog_state_cache.pop() if self._dialog_state_cache else None

    def read_recent_dialog_state(self):
        if len(self._dialog_state_cache) == 0:
            return None
        return self._dialog_state_cache[-1]

    def clear(self):
        self._dialog_state_cache.clear()
        return self._dialog_state_cache
