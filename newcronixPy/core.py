import threading
import time
from datetime import datetime
from .executor import run_task

_tasks = []
_lock = threading.Lock()
_running = False


def start():
    global _running
    if not _running:
        _running = True
        threading.Thread(target=_loop, daemon=True).start()


def stop():
    global _running
    _running = False


def add_task(task):
    with _lock:
        _tasks.append(task)


def _loop():
    global _running
    while _running:
        now = datetime.now()
        to_remove = []

        with _lock:
            for task in _tasks:
                if task.cancelled:
                    to_remove.append(task)
                    continue

                if task.should_run(now):
                    run_task(task.func, task.args)
                    task.last_run = now

                    task.run_count += 1

                    if task.repeat is not None and task.run_count >= task.repeat:
                        task.cancelled = True
                        to_remove.append(task)
                        continue

                    if task.one_time:
                        to_remove.append(task)

            for t in to_remove:
                if t in _tasks:
                     _tasks.remove(t)

        time.sleep(0.5)