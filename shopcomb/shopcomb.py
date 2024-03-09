"""Base module for scraping shopping sites
"""
import os
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class Shopcomb():
    """The base class for scrapping shopping sites
    All scrappers for shopping site must inherit this class

    - store_url - The store base url itself e.g https://amazon.com
    - query_url - The store url with an empty query param e.g https://amazon.com/s?k=
    - props - The peculiar properties needed for navigating the store. to be explained later
    """
    store_url = None
    query_url = None
    product_card_selector = None
    product_title_selector = None
    product_price_selector = None
    product_url_selector = None
    product_image_selector = None
    product_rating_selector = None

    def __init__(self) -> None:
        # Initialise attributes
        # self.store_url = store_url
        # self.query_url = query_url
        # self.product_card_selector = product_card_elem['product_card_selector']
        # self.product_title_selector = product_card_elem['product_title_selector']
        # self.product_url_selector = product_card_elem['product_url_selector']
        # self.product_image_selector = product_card_elem['product_image_selector']
        # self.product_rating_selector = product_card_elem['product_rating_selector']

        # Start Selenium
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        current_dir_path = os.path.dirname(os.path.abspath(__file__))
        chrome_bin_location = os.path.join(current_dir_path, "chrome/opt/google/chrome/google-chrome")
        driver_path = os.path.join(current_dir_path, 'chromedriver')
        chrome_service = Service(executable_path=driver_path)
        chrome_options.binary_location = chrome_bin_location
        self.driver = webdriver.Chrome(
            service=chrome_service, options=chrome_options)
 
    def form_search_url(self, query: str):
        """Return the complete search url using the query and the query url of the class
        e.g https://amazon.com/s?k=blue+bag
        Some sites have a different way of making search queries ensure to overide this
        method to take care of them.
        """
        query = "+".join(query.split(' '))
        search_url = f"{self.query_url}{query}"
        return search_url
    
    def get_price(self, product_card: WebElement):
        """Returns the actual and complete price of a product. Some site render
        their prices in unusual manners, overide this method to take care of them
        """
        return product_card.find_element(By.CSS_SELECTOR, self.product_price_selector).text
        
    
    def search_product(self, query: str):
        """Search for a product in the shopping site using a query.
        Returns a list of products found and their attributes
        """
        search_url = self.form_search_url(query)
        # Seacrh for product
        self.driver.get(search_url)
        # Wait to load
        print('product card', self.product_card_selector)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.product_card_selector)))
        
        # Safe wait
        WebDriverWait(self.driver, 2)
        # Get all the product cards
        product_cards = self.driver.find_elements(By.CSS_SELECTOR, self.product_card_selector)
        # Get product details from each product card
        products = []
        for product_card in product_cards:
            # Get product title
            products.append ({
                'product_title': product_card.find_element(By.CSS_SELECTOR, self.product_title_selector).text,
                'product_url': product_card.find_element(By.CSS_SELECTOR, self.product_url_selector).get_attribute('href'),
                'product_image': product_card.find_element(By.CSS_SELECTOR, self.product_image_selector).get_attribute('src'),
                'product_price': product_card.find_element(By.CSS_SELECTOR, self.product_price_selector).text,
                # 'product_rating': product_card.find_element(By.CSS_SELECTOR, self.product_rating_selector).text
            })
        return products


