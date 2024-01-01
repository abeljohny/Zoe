import datetime
import re

from constants import Intent, Prompts, Regex, Reprompts, Tags
from intent_handlers.intentABC import IntentABC
from util import Util


class Introspect(IntentABC):
    def __init__(self, config, memory, user):
        super().__init__()
        self._config = config
        self._memory = memory
        self._user = user
        self._calendar = self._memory.calendar

    def _events_from_request(self, request):
        dt = Util.parse_relative_time_expression(request)
        if dt:
            end_datetime = dt + datetime.timedelta(days=1, microseconds=-1)
            return self._calendar.events_between(dt, end_datetime), False

        matches = re.findall(Regex.DATE_ONLY_PATTERN.value, request)

        if not matches:
            return None, True

        date1, date2 = None, None
        if matches[0]:
            date1 = datetime.datetime(
                year=int(matches[0][2]),
                month=int(matches[0][0]),
                day=int(matches[0][1]),
            )
        if len(matches) > 1:
            date2 = datetime.datetime(
                year=int(matches[1][2]),
                month=int(matches[1][0]),
                day=int(matches[1][1]),
            )

        if date2 is None:
            if date1:
                return self._calendar.events_from(date1), False
            else:
                return None, True

        return self._calendar.events_between(date1, date2), False

    def handle(self, request, intent, dialog_state=None) -> str:
        selected_events, date_missing = self._events_from_request(request)

        if date_missing:
            ds = self._memory.initialize_dialog_state(
                intent=Intent.INTROSPECT.value,
                tag=Tags.DATE.value,
            )
            self._memory.enqueue_dialog_state(ds)
            reply = Prompts.INTROSPECT_EVENT_DATE.value
            if dialog_state and dialog_state["data"]["tag"] == Tags.DATE.value:
                reply = (
                    Reprompts.DIDNT_UNDERSTAND.value
                    + reply
                    + " "
                    + Prompts.HINT_DATE.value
                )
            return reply

        if len(selected_events) == 0:
            return Prompts.NO_EVENTS_FOUND.value

        if len(selected_events) >= self._config.MAX_EVENTS_TO_SHOW:
            return (
                f"I've found {len(selected_events)} scheduled events, but displaying all of them at once might be "
                f"overwhelming."
            )

        reply = f"I've found {len(selected_events)} event(s):"
        for event in selected_events:
            reply += "\n"
            reply += f"{event.name} from {event.start_datetime_formatted} to {event.end_datetime_formatted}"

        return reply

    def continue_conversation(self, request, intent) -> str:
        recent_dialog_state = self._memory.dequeue_dialog_state()
        return self.handle(request, Intent.INTROSPECT.value, recent_dialog_state)
