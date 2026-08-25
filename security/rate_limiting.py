import time


def middleware_rate_limit(request, rate_limit: int, time_window: int):
    ip = request.client.host
    current_time = time.time()

    if ip is None or current_time -  > :