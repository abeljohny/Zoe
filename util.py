import datetime
import re
import string
from datetime import timedelta

from constants import RELATIVE_TIME_EXPR_FUTURE


class Util(object):
    @staticmethod
    def rm_special_chars(text: str) -> str:
        """Normalize text to remove special characters"""
        custom_punctuation = string.punctuation.replace(".", "")
        custom_punctuation += "—" + "_" + "’" + "-" + "‘"

        return "".join([ch for ch in text if ch not in custom_punctuation])

    @staticmethod
    def text_contains_only_special(text):
        pattern = r"[^\W\d_]"
        return not bool(re.search(pattern, text))

    @staticmethod
    def convert_timestr_to_int(timestr):
        if timestr is None or timestr == "":
            return 0
        if isinstance(timestr, int):
            return timestr
        return int(timestr) if timestr.isdigit() else None

    @staticmethod
    def read_info(prompt):
        while True:
            info = input(f"{prompt} ")
            if info:
                if input("Do you wish to confirm your entry? [Y]: ") == "Y":
                    break
        return info

    @staticmethod
    def parse_time(request, pattern):
        from_hours, from_mins, from_ampm = None, None, None
        match_start_time = pattern.search(request)
        if match_start_time:
            from_hours, from_mins, from_ampm = (
                match_start_time.group("hours"),
                match_start_time.group("mins"),
                match_start_time.group("ampm"),
            )
        return from_hours, from_mins, from_ampm

    @staticmethod
    def parse_relative_time_expression(request):
        today = datetime.datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        tomorrow = today + timedelta(days=1)
        day_after = today + timedelta(days=2)
        for expr in RELATIVE_TIME_EXPR_FUTURE:
            if expr in request:
                match expr:
                    case "today":
                        return today
                    case "tomorrow" | "next day":
                        return tomorrow
                    case "day after":
                        return day_after
        return None

    @staticmethod
    def parse_date(request, pattern):
        date = None
        match_date = pattern.search(request)
        if match_date:
            month, day, year = (
                match_date.group("month"),
                match_date.group("day"),
                match_date.group("year"),
            )
            date = datetime.datetime(int(year), int(month), int(day))
        if date is None:
            date = Util.parse_relative_time_expression(request)

        return date

    @staticmethod
    def to_time(hours, mins, ampm):
        hours = Util.convert_timestr_to_int(hours)
        mins = Util.convert_timestr_to_int(mins)

        # convert event start hour to 24-hour time
        if ampm:
            hours = Util.convert_hour_to_24_hour_time(
                hours, True if ampm == "am" else False
            )

        return datetime.time(hours, mins)

    @staticmethod
    def to_date(month, day, year):
        if month and day and year:
            return datetime.date(int(year), int(month), int(day))

    @staticmethod
    def convert_hour_to_24_hour_time(hour, is_am):
        if is_am:
            if hour == 12:
                hour = 0
        else:
            if hour != 12:
                hour += 12
        return hour
