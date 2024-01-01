import datetime

from constants import (
    Intent,
    Prompts,
    RELATIVE_TIME_EXPR_PAST,
    Regex,
    Reprompts,
    Tags,
)
from event import Event
from intent_handlers.intentABC import IntentABC
from util import Util


class Book(IntentABC):
    def __init__(self, config, memory, user):
        super().__init__()
        self._config = config
        self._memory = memory
        self._calendar = memory.calendar
        self._user = user

    @staticmethod
    def parse_temporal_dat(request):
        from_hours, from_mins, from_ampm = Util.parse_time(
            request, Regex.START_TIME_PATTERN.value
        )
        if not from_hours:
            from_hours, from_mins, from_ampm = Util.parse_time(
                request, Regex.TIME_PATTERN.value
            )

        to_hours, to_mins, to_ampm = Util.parse_time(
            request, Regex.END_TIME_PATTERN.value
        )
        date = Util.parse_date(request, Regex.DATE_PATTERN.value)

        if from_ampm:
            from_ampm = from_ampm.lower()
        if to_ampm:
            to_ampm = to_ampm.lower()

        return from_hours, from_mins, from_ampm, to_hours, to_mins, to_ampm, date

    def handle(self, request, intent, dialog_state=None):
        # extract temporal information from request / previous dialogue state - start and end times + date
        if dialog_state:
            if dialog_state["data"]["time_start"]:
                from_hours, from_mins, from_ampm = (
                    dialog_state["data"]["time_start"].hour,
                    dialog_state["data"]["time_start"].minute,
                    None,
                )
            else:
                from_hours, from_mins, from_ampm = None, None, None

            if dialog_state["data"]["time_end"]:
                to_hours, to_mins, to_ampm = (
                    dialog_state["data"]["time_end"].hour,
                    dialog_state["data"]["time_end"].minute,
                    None,
                )
            else:
                to_hours, to_mins, to_ampm = None, None, None

            date = dialog_state["data"]["date"]
            appointment_name = dialog_state["data"]["appointment"]

        else:
            (
                from_hours,
                from_mins,
                from_ampm,
                to_hours,
                to_mins,
                to_ampm,
                date,
            ) = Book.parse_temporal_dat(request)
            appointment_name = None

            # check if event is in the past
            if any(expr in request for expr in RELATIVE_TIME_EXPR_PAST):
                return Prompts.BOOK_PAST_EVENT.value

        ds_tag = None

        # check if event start time provided
        time_start = None
        if from_hours is None:
            ds_tag = Tags.START_TIME.value
        else:
            # determine event start time
            time_start = Util.to_time(from_hours, from_mins, from_ampm)

        # determine event date
        if date is None and not ds_tag:
            ds_tag = Tags.DATE.value

        datetime_start = None
        if date and time_start:
            datetime_start = datetime.datetime.combine(date, time_start)

        # determine event end time
        datetime_end = None
        if datetime_start and to_hours is None:
            datetime_end = datetime_start + datetime.timedelta(minutes=30)
        elif to_hours:
            time_end = Util.to_time(to_hours, to_mins, to_ampm)
            if not to_ampm and time_end and time_end.hour >= 12:
                time_end = Util.to_time(to_hours, to_mins, to_ampm)
            if date and time_end:
                datetime_end = datetime.datetime.combine(date, time_end)

        # determine appointment name
        if appointment_name is None:
            appointment_name = Regex.APPOINTMENT_PATTERN.value.search(request)
            appointment_name = (
                appointment_name.group("appointment") if appointment_name else None
            )

        if appointment_name is None and not ds_tag:
            ds_tag = Tags.APPOINTMENT.value

        # record dialogue state and reprompt
        if ds_tag:
            ds = self._memory.initialize_dialog_state(
                intent=Intent.BOOK.value,
                tag=ds_tag,
                time_start=time_start,
                time_end=datetime_end.time() if datetime_end else None,
                appointmment=appointment_name,
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
                    reply += Prompts.REQUEST_TIME_FROM.value
                    if self._user.is_new_user:
                        reply += " " + Prompts.HINT_TIME.value

                case Tags.DATE.value:
                    if dialog_state and dialog_state["data"]["tag"] == Tags.DATE.value:
                        reply += Reprompts.DIDNT_UNDERSTAND.value
                    reply += Prompts.REQUEST_DATE.value
                    if self._user.is_new_user:
                        reply += " " + Prompts.HINT_DATE.value

                case Tags.APPOINTMENT.value:
                    reply += Prompts.REQUEST_APPOINTMENT_NAME.value

            return reply

        if (
            datetime_start < datetime.datetime.now()
            or datetime_end < datetime.datetime.now()
        ):
            return Prompts.BOOK_PAST_EVENT.value

        # record event in calendar if there's no time conflict with another event
        is_conflict = self._calendar.add_event(
            Event(
                name=appointment_name,
                start_datetime=datetime_start,
                end_datetime=datetime_end,
            )
        )
        if is_conflict:
            return Prompts.CONFLICT_APPOINTMENT.value

        if appointment_name.startswith('"') and appointment_name.endswith('"'):
            reply = f"{appointment_name} is scheduled."
        else:
            reply = f'"{appointment_name}" is scheduled.'

        if self._user.is_new_user and dialog_state:
            reply += f' Alternatively, You may also book this event by specifying a time and date: Please book {appointment_name} from {datetime_start.strftime("%I:%M%p")} to {datetime_end.strftime("%I:%M%p")} on {datetime_start.date().strftime("%m/%d/%Y")}.'

        return reply

    def continue_conversation(self, request, intent):
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

            case Tags.APPOINTMENT.value:
                if not request.startswith('"') and not request.endswith('"'):
                    request = f'"{request}"'

        return self.handle(request, Intent.BOOK.value, recent_dialog_state)
