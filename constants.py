import re
from enum import Enum


class Intent(Enum):
    GREETING = "greeting"
    BOOK = "book"
    CANCEL = "cancel"
    INTROSPECT = "introspect"
    SMALLTALK = "smalltalk"
    NAMEOPS = "nameops"
    LOW_CONFIDENCE = "low_confidence"


class Commands(Enum):
    EXIT = "exit"
    ABORT = "abort"


RELATIVE_TIME_EXPR_FUTURE = [
    "today",
    "tomorrow",
    "next day",
    "day after",
]

RELATIVE_TIME_EXPR_PAST = [
    "yesterday",
    "day before",
    "previous day",
    "previos day",
    "past day",
    "last week",
    "previous week",
    "previos week",
]


class Regex(Enum):
    TIME_PATTERN = re.compile(
        r"(?i)(?P<hours>[0-9]{1,2})[:.]?(?P<mins>[0-9]{0,2})? *(?P<ampm>am|pm)?"
    )
    START_TIME_PATTERN = re.compile(
        r"(?i)(at|from|for|my) *(?P<hours>[0-9]{1,2})[:.]?(?P<mins>[0-9]{0,2})? *(?P<ampm>am|pm)?"
    )
    END_TIME_PATTERN = re.compile(
        r"(?i)(to) *(?P<hours>[0-9]{1,2})[:.]?(?P<mins>[0-9]{0,2})? *(?P<ampm>am|pm)?"
    )
    DATE_PATTERN = re.compile(
        r"(on) *(?P<month>[0-9]{1,2})\/(?P<day>[0-9]{1,2})\/(?P<year>[0-9]{4})"
    )
    DATE_ONLY_PATTERN = re.compile(
        r"(?P<month>[0-9]{1,2})\/(?P<day>[0-9]{1,2})\/(?P<year>[0-9]{4})"
    )
    APPOINTMENT_PATTERN = re.compile(r'(?P<appointment>"(.*?)")', re.IGNORECASE)


class Tags(Enum):
    USER = "user"
    BOT = "bot"
    DATE = "date"
    APPOINTMENT = "appointment"
    START_TIME = "start_time"


class ConversationalMarkers(Enum):
    AND = "And "
    TO_CONFIRM = "Just to confirm, "


class Reprompts(Enum):
    DIDNT_UNDERSTAND = "I’m sorry, I didn’t understand. "

    REPEAT = "Oops, I missed that. Could you please repeat?"

    REPHRASE = "Sorry, I don't understand. Can you please rephrase?"


class Prompts(Enum):
    STARTUP = """Hello! I'm Zoe, your personal scheduling assistant. I'm here to help you make the most of your \
time by managing your calendar and scheduling your appointments. 
Could you tell me your name please?"""

    ABORT = "ABORTED"

    ACTION = "Would you like me to book, cancel, or search an event for you today?"

    ACTION_NEW_USER = (
        "Would you like me to book, cancel, or search an event for you today? (Simply type 'book', 'cancel' or "
        "'search')"
    )

    HELPCMD = (
        "(Keep in mind, you can type 'abort' to conclude a conversation you wish to discontinue and 'exit' to "
        "conclude our interaction.)"
    )

    BOOK_PAST_EVENT = "Sorry, I can't make an appointment in the past."

    REQUEST_DATE = "Which date do you prefer for booking?"

    HINT_DATE = (
        "Please enter it in the format MM/DD/YYYY. Alternatively, you can use phrases like 'today',"
        "'tomorrow', or 'day after'."
    )

    REQUEST_TIME_FROM = "What time would you like to schedule this event?"

    HINT_TIME = "For instance, you may enter 10am or 12.30pm."

    REQUEST_APPOINTMENT_NAME = "what would you like to call it?"

    NO_EVENTS_FOUND = "You have no events scheduled then."

    CANCEL_EVENT_START_TIME = "what time was this event scheduled for?"

    CANCEL_EVENT_DATE = "what date was this event scheduled for?"

    NO_EVENT_TO_CANCEL = "I couldn't find an event for that date and time."

    EVENT_CANCELLED = "OK, it's cancelled."

    EVENT_CANCEL_ABORTED = "OK, I won't cancel the event."

    INTROSPECT_EVENT_DATE = "What dates are scheduled for the event?"

    CONFLICT_APPOINTMENT = (
        "It seems you have another event at this slot. Please cancel this apppointment before booking "
        "another one at the same slot."
    )

    HINT_INTROSPECT_DATE = (
        "Please enter it in the format MM/DD/YYYY. Alternatively, you can use phrases like 'today', "
        "'tomorrow', or 'day after'. You may also specify a range like 12/23/2023 to 12/25/2023."
    )
