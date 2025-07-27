# import sys
# import re 
# import random
# sys.path.append(r'G:\My Drive\ecommerce_loadtest')
# from locust import HttpUser,task , SequentialTaskSet,between,events
# from utils.custom_logger import logger
# from test_data.read_test_data import CsvRead
# from load_patterns.stages_pattern import StagesShape


# class Loadtest(SequentialTaskSet):
    
#     def __init__(self,parent):
#         super().__init__(parent)
#         # self.sessionid = ""
#         # self.product = ""
    
#     @events.test_start.add_listener
#     def on_test_start(environment, **kwargs):
#         print("....................LOAD TEST STARTED.................................")
        

#     @task
#     def homepage(self):
#         with self.client.get("", catch_response = True, name = "GET/Homepage") as response : 
#             if "Full-Fledged practice website for Automation Engineers" in response.text and response.status_code == 200:
#                 response.success()
#                 logger.info('Homepage loaded successfully')
#             else: 
#                 response.fail('Homepage took long to load or text check failed')
#                 logger.error('Homepage failed to load')
    
#     @task
#     def loginPage(self):
#         with self.client.get('/login', catch_response=True, name='GET/loginpage') as response:
#             if response.status_code == 200:
#                 csrf_token = re.search(r"name=\"csrfmiddlewaretoken\" value=\"([^\"]+)\"", response.text)
#                 if csrf_token:
#                     self.csrf_token = csrf_token.group(1)
#                     print(f"CSRF Token: {csrf_token}")  # Print the token
#                     response.success()
#                     logger.info('Login page loaded successfully')
#                 else:
#                     response.failure("Missing CSRF form token")
                    
            
#     @task
#     def create_account(self):
#          # Step 2: Load user data from CSV
#         signup_data = CsvRead("test_data/signup-data.csv").read()
#         print(signup_data)

#         user_payload = {
#             "csrfmiddlewaretoken": self.csrf_token,
#             "name": signup_data["name"],
#             "email_address": signup_data["email_address"],
#             "password": signup_data["password"],
#             "days": signup_data["days"],
#             "months": signup_data["months"],
#             "years": signup_data["years"],
#             "first_name": signup_data["first_name"],
#             "last_name": signup_data["last_name"],
#             "company": signup_data["company"],
#             "address1": signup_data["address1"],
#             "address2": signup_data["address2"],
#             "country": signup_data["country"],
#             "state": signup_data["state"],
#             "city": signup_data["city"],
#             "zipcode": signup_data["zipcode"],
#             "mobile_number": signup_data["mobile_number"],
#             "form_type": 'create_account'
#         }

#         headers = {
#             "Referer": "https://www.automationexercise.com/signup",
#             "Content-Type": "application/x-www-form-urlencoded"
#         }

#         # Step 3: Submit form
#         with self.client.post('/signup', data=user_payload, headers=headers, catch_response=True, name='POST/signup') as response:
#             if 'Account Created!' in response.text:
#                 response.success()
#                 logger.info('Signup successful')
#             else:
#                 response.failure('Signup failed')
#                 logger.error('Signup failed')

    
#     @task
#     def Signin(self):
#         url = '/login'
        
#         data ={
#         'csrfmiddlewaretoken' : self.csrf_token,
#         'email' : 'noxehoj388@utliz.com',
#         'password' : 'Bbbvj5GTfCkr@n' 
#         }
        
#         headers ={
#             'referer' :'https://www.automationexercise.com/login',
#             'Content-Type': 'application/x-www-form-urlencoded'
#         }
#         with self.client.post(url, data=data, headers=headers, catch_response=True, name='POST/login') as response:
#             if "Logged in as" in response.text:
#                 response.success()
#                 logger.info('Login successful')
#             else:
#                 response.failure("Login failed")
    
#     @task
#     def Produts(self):
#         with self.client.get('/products', catch_response=True, name='GET/products') as response:
#             if 'All Products' in response.text and response.status_code == 200:
#                 response.success()
#                 logger.info('Products page loaded successfully')
#             else:
#                 response.failure('Failed to load products page')
#                 logger.error('Failed to load products page')

#     @task
#     def search_Product(self):
#         search_term = random.choice(["Tshirt", "Jeans", "Dress", "Top", "Shirt"])
#         url = f"/products?search={search_term}"
#         with self.client.get(url, catch_response=True, name='GET/Search_products') as response:
#             if 'Searched Products' in response.text and response.status_code == 200:
#                 response.success()
#                 logger.info('Products page loaded successfully')
#             else:
#                 response.failure('Failed to load products page')
#                 logger.error('Failed to load products page')
    
#     @task
   
#     def view_and_add_product(self):
#         # Get real product ID
#         with self.client.get("/products", catch_response=True, name="GET/products") as response:
#             product_ids = re.findall(r'/product_details/(\d+)', response.text)
#             product_ids = list(set(product_ids))
#             if not product_ids:
#                 response.failure("No product IDs found")
#                 logger.error("No product IDs found")
#                 return

#             product_id = random.choice(product_ids)

#         # Go to product detail
#         with self.client.get(f"/product_details/{product_id}", catch_response=True, name='GET/view_product') as response:
#             if 'Add to cart' not in response.text:
#                 response.failure("Product detail did not load properly")
#                 return

#             quantity = random.randint(1, 3)
#             add_url = f"/add_to_cart/{product_id}?quantity={quantity}"

#             with self.client.get(add_url, name="GET/add_to_cart", catch_response=True) as response:
            
#                 if "Cart" in response.text or "Continue Shopping" in response.text:
#                     self.cart_has_items = True
#                     response.success()
#                     logger.info('Product added to cart successfully')
                    
                    
#                 else:
#                     self.cart_has_items = False
#                     response.failure(f"Add to cart failed for product {product_id}")
                    
#                     print("[DEBUG] Add-to-cart response:\n", response.text[:500])

#     @task 
#     def view_cart(self):
#         with self.client.get('/view_cart', catch_response=True, name='GET/view_cart') as response:
#             if any(term in response.text for term in ["Proceed To Checkout", "Shopping Cart", "Cart Items"]):
#                 response.success()
#                 logger.info('View Cart page loaded successfully')
#             else:
#                 response.failure("View Cart content check failed")
#                 logger.error('Failed to load View Cart page')

#             # Debugging aid
#             if "Cart is empty!" in response.text:
#                 print("[DEBUG] Cart is empty - possibly product was not added.")

#     @task
#     def checkout_and_payment(self):
#         with self.client.get('/checkout', catch_response=True, name='GET/checkout') as response:
#             token_match = re.search(r'name="csrfmiddlewaretoken"\s+value="(.+?)"', response.text)
#             if not token_match:
#                 response.failure()
#                 logger.error("No CSRF token on checkout")
#                 return
#             token = token_match.group(1)
        
#             payment = CsvRead("test_data\\payment-data.csv").read()
#             print(payment)

#             payment_data = {
#                     "csrfmiddlewaretoken": token,
#                     "name_on_card": payment["name_on_card"],
#                     "card_number": payment["card_number"],
#                     "cvc": payment["cvc"],
#                     "expiry_month": payment["expiry_month"],
#                     "expiry_year": payment["expiry_year"]
#                 }
            
        
#             headers = {
#                 "Referer": "https://www.automationexercise.com/payment"
#             }

#         with self.client.post('/payment', data=payment_data, headers=headers, catch_response=True, name='POST/checkout') as response:
#             if 'Congratulations! Your order has been confirmed!' in response.text and response.status_code == 200:
#                 response.success()  
#                 logger.info('Checkout successful')
#             else:
#                 response.failure('failed to checkout')
#                 logger.error('failed to checkout')
    
# class WebsiteUser(HttpUser):
#     host = 'https://www.automationexercise.com'
#     wait_time = between(1, 5)
#     tasks = [Loadtest]