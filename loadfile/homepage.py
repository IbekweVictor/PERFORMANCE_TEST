from locust import task, SequentialTaskSet
from utils.custom_logger import logger

class Homepage(SequentialTaskSet):

    @task
    def homepage(self):
        with self.client.get("", catch_response=True, name="GET/Homepage") as response:
            if "Full-Fledged practice website for Automation Engineers" in response.text and response.status_code == 200:
                response.success()
                logger.info("Homepage loaded")
            else:
                response.failure("Homepage failed")
                logger.error("Homepage check failed")
