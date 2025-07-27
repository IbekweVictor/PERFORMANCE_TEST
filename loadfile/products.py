import re
import random
from locust import task, SequentialTaskSet
from utils.custom_logger import logger

class Product(SequentialTaskSet):

    @task
    def view_products(self):
        with self.client.get('/products', catch_response=True, name='GET/products') as response:
            if 'All Products' in response.text:
                response.success()
                logger.info("roducts page loaded")
            else:
                response.failure("Failed to load products page")
                logger.error(f"Products page failure: {response.status_code}")

    @task
    def search_products(self):
        search_term = random.choice(["Tshirt", "Jeans", "Dress", "Top", "Shirt"])
        with self.client.get(f"/products?search={search_term}", catch_response=True, name='GET/Search_products') as response:
            if 'Searched Products' in response.text:
                response.success()
                logger.info(f"Searched for {search_term}")
            else:
                response.failure("Product search failed")
                logger.error(f"Search for {search_term} failed")

    @task
    def view_and_add_product(self):
        # Step 1: Fetch real product IDs
        with self.client.get('/products', catch_response=True, name='GET/products_for_cart') as response:
            product_ids = re.findall(r'/product_details/(\d+)', response.text)
            if not product_ids:
                response.failure("No product IDs found")
                logger.warning("No products available to add")
                return

            selected_id = random.choice(product_ids)
            logger.debug(f"Selected product ID: {selected_id}")

        # Step 2: Load product detail page
        detail_url = f"/product_details/{selected_id}"
        with self.client.get(detail_url, catch_response=True, name='GET/view_product') as detail_response:
            if 'Add to cart' not in detail_response.text:
                detail_response.failure("Product detail page missing 'Add to cart'")
                logger.warning(f"Product {selected_id} page incomplete")
                return

       
        # Step 3: Add to cart
        quantity = random.randint(1, 3)
        add_url = f"/add_to_cart/{selected_id}?quantity={quantity}"
        with self.client.get(add_url, name="GET /add_to_cart", catch_response=True) as response:
            if any(phrase in response.text for phrase in [
                "Added!",
                "View Cart",
                "Continue Shopping",
                "Added To Cart",
                "Your product has been added to cart"
            ]):
                response.success()
                self.user.cart_has_items = True
                logger.info(f"Added product {selected_id} (qty: {quantity}) to cart")
            else:
                response.failure("Add to cart failed")
                logger.error(f"Failed to add product {selected_id}. Response: {response.text[:200]}")
