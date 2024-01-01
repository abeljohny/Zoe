from event import Event


class Calendar(object):
    def __init__(self, config):
        self._config = config
        self._events = []

    def check_conflict(self, event) -> bool:
        """
        Returns if the input event has a conflict with existing events.
        :param event: Event object to save
        :return: boolean indicating if there is a conflict
        """
        if not self._events:
            return False

        for ev in self._events:
            if (
                event.start_datetime >= ev.start_datetime
                and event.end_datetime <= ev.end_datetime
            ):
                return True

    def read_event(self, event):
        if not self._events:
            return None

        for ev in self._events:
            if ev.start_datetime == event.start_datetime:
                return ev
        return None

    def add_event(self, event: Event) -> bool:
        if self.check_conflict(event):
            return True
        self._events.append(event)
        self._events.sort(key=lambda x: x.start_datetime)

    def events_at(self, datetime):
        selected_events = []
        for event in self._events:
            if event.start_datetime == datetime:
                selected_events.append(event)
        return selected_events

    def events_from(self, date):
        for event in self._events:
            if event.start_datetime == date:
                return [event]
        return []

    def events_between(self, date1, date2):
        selected_events = []

        if date1 <= date2:
            start_date = date1
            end_date = date2
        else:
            start_date = date2
            end_date = date1

        for event in self._events:
            if start_date <= event.start_datetime and event.end_datetime <= end_date:
                selected_events.append(event)
        return selected_events

    def cancel_event(self, event):
        self._events.remove(event)
