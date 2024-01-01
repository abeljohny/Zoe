import datetime

from constants import ConversationalMarkers, Intent, Prompts, Regex, Reprompts, Tags
from intent_handlers.book import Book
from intent_handlers.intentABC import IntentABC
from util import Util


class Cancel(IntentABC):
    def __init__(self, config, memory, user):
        super().__init__()
        self._config = config
        self._memory = memory
        self._user = user
        self._calendar = memory.calendar

    def handle(self, request, intent, dialog_state=None) -> str:
        ds_tag = None

        if dialog_state:
            if dialog_state["data"]["time_start"]:
                from_hours, from_mins, from_ampm = (
                    dialog_state["data"]["time_start"].hour,
                    dialog_state["data"]["time_start"].minute,
                    None,
                )
            else:
                from_hours, from_mins, from_ampm = None, None, None

            date = dialog_state["data"]["date"]

        else:
            (
                from_hours,
                from_mins,
                from_ampm,
                _,
                _,
                _,
                date,
            ) = Book.parse_temporal_dat(request)

        time_start = None
        if from_hours is None:
            ds_tag = Tags.START_TIME.value
        else:
            time_start = Util.to_time(from_hours, from_mins, from_ampm)

        if date is None and not ds_tag:
            ds_tag = Tags.DATE.value

        # record dialogue state and reprompt
        if ds_tag:
            ds = self._memory.initialize_dialog_state(
                intent=Intent.CANCEL.value,
                tag=ds_tag,
                time_start=time_start,
                date=date,
            )
            self._memory.enqueue_dialog_state(ds)

            reply = ""
            match ds_tag:
                case Tags.START_TIME.value:
                    if (
                        dialog_state
                        and dialog_state["data"]["tag"] == Tags.START_TIME.value
                    ):
                        reply += Reprompts.DIDNT_UNDERSTAND.value
                    else:
                        reply += ConversationalMarkers.TO_CONFIRM.value

                    reply += Prompts.CANCEL_EVENT_START_TIME.value
                    if self._user.is_new_user:
                        reply += " " + Prompts.HINT_TIME.value

                    return reply

                case Tags.DATE.value:
                    if dialog_state and dialog_state["data"]["tag"] == Tags.DATE.value:
                        reply += Reprompts.DIDNT_UNDERSTAND.value
                    else:
                        reply += ConversationalMarkers.AND.value

                    reply += Prompts.CANCEL_EVENT_DATE.value
                    if self._user.is_new_user:
                        reply += " " + Prompts.HINT_DATE.value

                    return reply

        if date and time_start:
            event_to_cancel = self._calendar.events_at(
                datetime.datetime.combine(date, time_start)
            )
            if not event_to_cancel:
                return Prompts.NO_EVENT_TO_CANCEL.value

        prompt = input(f"Do you wish to cancel {event_to_cancel[0].name}? [Y]: ")
        if prompt == "Y":
            self._calendar.cancel_event(event_to_cancel[0])
            reply = Prompts.EVENT_CANCELLED.value
            if self._user.is_new_user and dialog_state:
                reply += f' Alternatively, You may also cancel this event by specifying a time and date: Cancel my {time_start.strftime("%I:%M%p")} on {date.strftime("%m/%d/%Y")}.'
            return reply

        return Prompts.EVENT_CANCEL_ABORTED.value

    def continue_conversation(self, request, intent) -> str:
        recent_dialog_state = self._memory.dequeue_dialog_state()
        match recent_dialog_state["data"]["tag"]:
            case Tags.START_TIME.value:
                from_hours, from_mins, from_ampm = Util.parse_time(
                    request, Regex.TIME_PATTERN.value
                )
                if from_hours:
                    recent_dialog_state["data"]["time_start"] = Util.to_time(
                        from_hours, from_mins, from_ampm
                    )

            case Tags.DATE.value:
                date = Util.parse_date(request, Regex.DATE_PATTERN.value)
                if not date:
                    date = Util.parse_date(request, Regex.DATE_ONLY_PATTERN.value)
                recent_dialog_state["data"]["date"] = date

        return self.handle(request, Intent.CANCEL.value, recent_dialog_state)
