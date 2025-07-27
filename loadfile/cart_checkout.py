import re
from locust import task, SequentialTaskSet
from test_data.read_test_data import CsvRead
from utils.custom_logger import logger

class Checkout(SequentialTaskSet):

    @task
    def view_cart(self):
        if not getattr(self.user, "cart_has_items", False):
            logger.warning("Skipping view_cart: No items in cart")
            return  # Skip if no item was added

        with self.client.get('/view_cart', catch_response=True, name='GET/view_cart') as response:
            if any(keyword in response.text for keyword in [
                "Proceed To Checkout", "Cart", "Price", "Quantity", "Continue Shopping"
            ]):
                response.success()
                logger.info("Cart viewed successfully")
            else:
                response.failure("Failed to view cart")
                logger.error("Cart page did not load expected content")


    @task
    def checkout_and_pay(self):
        with self.client.get('/checkout', catch_response=True, name='GET/checkout') as response:
            token_match = re.search(r'name="csrfmiddlewaretoken"\s+value="(.+?)"', response.text)
            if not token_match:
                response.failure("No CSRF token on checkout")
                return
            token = token_match.group(1)

        payment = CsvRead("test_data/payment-data.csv").read()
        payment_data = {
            "csrfmiddlewaretoken": token,
            "name_on_card": payment["name_on_card"],
            "card_number": payment["card_number"],
            "cvc": payment["cvc"],
            "expiry_month": payment["expiry_month"],
            "expiry_year": payment["expiry_year"]
        }

        headers = {
            "Referer": "https://www.automationexercise.com/payment"
        }

        with self.client.post('/payment', data=payment_data, headers=headers, catch_response=True, name='POST/checkout') as pay_response:
            if 'Congratulations! Your order has been confirmed!' in pay_response.text:
                pay_response.success()
                logger.info("Payment successful")
            else:
                pay_response.failure("Payment failed")
