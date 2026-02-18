import time


def generate_tag_pk():
    return str(time.time_ns())
