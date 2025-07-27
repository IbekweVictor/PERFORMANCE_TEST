# load_patterns/stages_pattern.py
from locust.shape import LoadTestShape

class StagesShape(LoadTestShape):
    """
    Multi-stage load pattern:
    - Gradually ramps up and down through defined stages.
    """
    stages = [
        {"duration": 60, "users": 10},     # 0–60s: 10 users
        {"duration": 100, "users": 50},    # 60–100s: 50 users
        {"duration": 180, "users": 100},   # 100–180s: 100 users
        {"duration": 220, "users": 30},    # 180–220s: 30 users
        {"duration": 240, "users": 10},    # 220–240s: 10 users
        {"duration": 260, "users": 1},     # 240–260s: 1 user
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], 100)  # spawn rate

        return None
