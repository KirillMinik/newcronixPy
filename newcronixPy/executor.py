from concurrent.futures import ThreadPoolExecutor

_executor = ThreadPoolExecutor(max_workers=10)


def run_task(func, args):
    def safe():
        try:
            func(*args)
        except Exception as e:
            print(f"[newcronixPy] Task error: {e}")

    _executor.submit(safe)