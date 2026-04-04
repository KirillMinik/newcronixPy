import time
from datetime import datetime


class BaseTask:
    def __init__(self, func, args):
        self.func = func
        self.args = args
        self.last_run = None
        self.cancelled = False
        self.one_time = False

    def should_run(self, now: datetime):
        raise NotImplementedError

    def cancel(self):
        self.cancelled = True


class IntervalTask(BaseTask):
    def __init__(self, interval, func, args):
        super().__init__(func, args)
        self.interval = interval
        self.next_run = time.monotonic() + interval

    def should_run(self, now):
        if time.monotonic() >= self.next_run:
            self.next_run = time.monotonic() + self.interval
            return True
        return False


class DailyTask(BaseTask):
    def __init__(self, hour, minute, func, args):
        super().__init__(func, args)
        self.hour = hour
        self.minute = minute

    def should_run(self, now):
        return (
            now.hour == self.hour
            and now.minute == self.minute
            and self.last_run != now.date()
        )


class WeeklyTask(BaseTask):
    def __init__(self, weekday, hour, minute, func, args):
        super().__init__(func, args)
        self.weekday = weekday
        self.hour = hour
        self.minute = minute

    def should_run(self, now):
        return (
            now.weekday() == self.weekday
            and now.hour == self.hour
            and now.minute == self.minute
            and self.last_run != now.date()
        )


class OneTimeTask(BaseTask):
    def __init__(self, run_at, func, args):
        super().__init__(func, args)
        self.run_at = run_at
        self.one_time = True

    def should_run(self, now):
        return time.monotonic() >= self.run_at