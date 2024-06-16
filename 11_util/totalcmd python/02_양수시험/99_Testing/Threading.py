import threading
import time


def timer_callback():
    print("Timer completed!")


def run_timer(seconds):
    timer = threading.Timer(seconds, timer_callback)
    timer.start()


# Example usage:
run_timer(10)  # Start a timer for 10 seconds


for i in range(20):
    print('this is just coun:', i)
    time.sleep(1)
