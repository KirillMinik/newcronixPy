import time
from .tasks import IntervalTask, DailyTask, WeeklyTask, OneTimeTask
from .core import add_task
from .utils import parse_time


class TaskBuilder:
    def __init__(self, mode, value=None):
        self.mode = mode
        self.value = value
        self.unit = None
        self.at_time = None
        self.weekday = None

    def seconds(self):
        self.unit = "seconds"
        return self

    def minutes(self):
        self.unit = "minutes"
        return self

    def hours(self):
        self.unit = "hours"
        return self

    def day(self):
        self.unit = "day"
        return self

    def monday(self): return self._set_weekday(0)
    def tuesday(self): return self._set_weekday(1)
    def wednesday(self): return self._set_weekday(2)
    def thursday(self): return self._set_weekday(3)
    def friday(self): return self._set_weekday(4)

    def _set_weekday(self, day):
        self.unit = "weekday"
        self.weekday = day
        return self

    def at(self, time_str):
        parse_time(time_str)
        self.at_time = time_str
        return self

    def do(self, func, *args):
        task = None

        if self.mode == "in":
            task = OneTimeTask(time.monotonic() + self.value, func, args)

        elif self.mode == "every" and self.unit in ["seconds", "minutes", "hours"]:
            mult = {"seconds": 1, "minutes": 60, "hours": 3600}[self.unit]
            task = IntervalTask(self.value * mult, func, args)

        elif self.mode == "every" and self.unit == "day":
            h, m = map(int, self.at_time.split(":"))
            task = DailyTask(h, m, func, args)

        elif self.mode == "every" and self.unit == "weekday":
            h, m = map(int, self.at_time.split(":"))
            task = WeeklyTask(self.weekday, h, m, func, args)

        if task:
            add_task(task)

        return task


def every(value=None):
    return TaskBuilder("every", value)


def in_(seconds):
    return TaskBuilder("in", seconds)