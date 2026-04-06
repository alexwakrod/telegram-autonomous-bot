import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests=5, window_seconds=10):
        self.max_requests = max_requests
        self.window = window_seconds
        self.user_requests = defaultdict(list)

    def is_allowed(self, user_id: int) -> bool:
        now = time.time()
        self.user_requests[user_id] = [t for t in self.user_requests[user_id] if now - t < self.window]
        if len(self.user_requests[user_id]) >= self.max_requests:
            return False
        self.user_requests[user_id].append(now)
        return True

rate_limiter = RateLimiter()