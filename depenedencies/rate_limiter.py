import time

class RateLimiter:
    def __init__(self, max_requests, window_time):
        self.requests = {}
        self.max_requests = max_requests
        self.window_time = window_time

    def is_allowed(self, client_id):
        current_time = time.time()
        request_info = self.requests.get(client_id)

        if request_info is None:
            self.requests[client_id] = [current_time, 1]
            return True

        last_request_time, request_count = request_info

        if current_time - last_request_time > self.window_time:
            self.requests[client_id] = [current_time, 1]
            return True

        if request_count < self.max_requests:
            self.requests[client_id][1] += 1
            return True

        return False