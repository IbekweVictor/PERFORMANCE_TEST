import re
import random
from locust import task, SequentialTaskSet
from test_data.read_test_data import CsvRead
from utils.custom_logger import logger


class Auth(SequentialTaskSet):

    @task
    def login_page(self):
        with self.client.get('/login', catch_response=True, name='GET/loginpage') as response:
            if response.status_code == 200:
                csrf_token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
                if csrf_token:
                    self.csrf_token = csrf_token.group(1)
                    logger.info("CSRF token acquired")
                    response.success()
                else:
                    response.failure("CSRF token not found in login page")
                    logger.error("CSRF token not found in login page")
            else:
                response.failure(f"Login page load failed: {response.status_code}")
                logger.error(f"Login page response: {response.status_code} | {response.text[:200]}")

    @task
    def create_account(self):
        signup_data = CsvRead("test_data/signup-data.csv").read()
        
        # Add random suffix to email to prevent reuse
        base_email = signup_data["email_address"]
        name_part, domain = base_email.split("@")
        unique_email = f"{name_part}_{random.randint(1000, 9999)}@{domain}"
        signup_data["email_address"] = unique_email
        logger.debug(f"Using signup email: {unique_email}")

        user_payload = {
            "csrfmiddlewaretoken": getattr(self, "csrf_token", ""),
            "name": signup_data["name"],
            "email_address": signup_data["email_address"],
            "password": signup_data["password"],
            "days": signup_data["days"],
            "months": signup_data["months"],
            "years": signup_data["years"],
            "first_name": signup_data["first_name"],
            "last_name": signup_data["last_name"],
            "company": signup_data["company"],
            "address1": signup_data["address1"],
            "address2": signup_data["address2"],
            "country": signup_data["country"],
            "state": signup_data["state"],
            "city": signup_data["city"],
            "zipcode": signup_data["zipcode"],
            "mobile_number": signup_data["mobile_number"],
            "form_type": 'create_account'
        }

        headers = {
            "Referer": "https://www.automationexercise.com/signup",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        with self.client.post('/signup', data=user_payload, headers=headers, catch_response=True, name='POST/signup') as response:
            if 'Account Created!' in response.text:
                response.success()
                logger.info('Signup successful')
            else:
                response.failure('Signup failed')
                logger.error(f'Signup failed response: {response.status_code} | {response.text[:300]}')

    @task
    def signin(self):
        data = {
            "csrfmiddlewaretoken": getattr(self, "csrf_token", ""),
            "email": "noxehoj388@utliz.com",
            "password": "Bbbvj5GTfCkr@n"
        }
        headers = {
            "Referer": "https://www.automationexercise.com/login",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        with self.client.post("/login", data=data, headers=headers, catch_response=True, name='POST/login') as response:
            if "Logged in as" in response.text:
                response.success()
                logger.info("Login successful")
            else:
                response.failure("Login failed")
                logger.error(f"Login failed: {response.status_code} | {response.text[:200]}")
