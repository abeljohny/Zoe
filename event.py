class Event(object):
    def __init__(self, name=None, start_datetime=None, end_datetime=None):
        self._event_name = name
        self._start_datetime = start_datetime
        self._end_datetime = end_datetime

    @property
    def name(self):
        return self._event_name

    @property
    def start_datetime(self):
        return self._start_datetime

    @property
    def start_datetime_formatted(self):
        return self._start_datetime.strftime("%H:%M")

    @property
    def end_datetime(self):
        return self._end_datetime

    @property
    def end_datetime_formatted(self):
        return self._end_datetime.strftime("%H:%M")
