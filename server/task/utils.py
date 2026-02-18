import time


def generate_task_pk():
    return str(time.time_ns())
