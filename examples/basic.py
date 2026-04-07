import newcronixPy as nc
import time

# ===================== functions =====================

def hello(msg):
    print(f"[HELLO] {msg}")

def counter():
    print("[COUNTER] tick")

def error_task():
    print("[ERROR] There will be an error now")
    raise ValueError("error test")

# ===================== start =====================

nc.start()

# ===================== times (added in 0.1.1) ===================

# 5 times every 2 seconds
t9 = nc.every(2).seconds.times(5).do(hello, "5 times every 2 seconds")

# 1 time (you can use once btw)
t10 = nc.every(10).seconds.times(1).do(hello, "1 time in 10 seconds")
# once using
t101 = nc.every(15).seconds.once.do(hello, "once time show message")

# infinity (default)
t11 = nc.every(1).minutes.do(hello, 'infinity times (basic)')

# ===================== intervals =====================

# every 2 seconds
t1 = nc.every(2).seconds.do(hello, "every 2 seconds")

# every 1 minute
t2 = nc.every(1).minutes.do(hello, "every minute")

# every 2 hours
t3 = nc.every(2).hours.do(hello, "every 2 hours")

# ===================== daily =====================

# every day at 12:00
t4 = nc.every(1).day.at("12:00").do(hello, "every day at 12:00")

# ===================== days of week =====================

# monday
t5 = nc.every().monday.at("10:00").do(hello, "monday 10:00")

# friday
t6 = nc.every().friday.at("18:00").do(hello, "friday 18:00")

# ===================== one-time =====================

# after 5 seconds
t7 = nc.in_(5).do(hello, "after 5 seconds")

# after 10 seconds
t8 = nc.in_(10).do(hello, "after 10 seconds")

# ===================== cancel task =====================

# cancel after 8 seconds
def cancel_task():
    print("[CANCEL] cancel t1 (every 2 sec)")
    t1.cancel()

nc.in_(8).do(cancel_task)

# ===================== error =====================

nc.in_(3).do(error_task)

# ===================== create task =====================

def create_task():
    print("[DYNAMIC] create new task (every 1 sec)")
    nc.every(1).seconds.do(counter)

nc.in_(6).do(create_task)

# ===================== stop scheduler =====================

def stop_scheduler():
    print("[STOP] stop scheduler")
    nc.stop()

# stop after 20 seconds
nc.in_(20).do(stop_scheduler)

# ===================== basic cycle !!!mandatory!!! DONT TOUCH!!! =====================

while True:
    time.sleep(1)