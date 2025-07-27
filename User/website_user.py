import sys
sys.path.append(r'G:\My Drive\ecommerce_loadtest')
from locust import HttpUser, between
from loadfile.homepage import Homepage
from loadfile.Auth import Auth
from loadfile.products import Product
from loadfile.cart_checkout import Checkout

class WebsiteUser(HttpUser):
    
    wait_time = between(1, 5)
    tasks = [Homepage, Auth, Product, Checkout]
