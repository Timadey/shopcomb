"""Base module for scraping shopping sites
"""
import os
from selenium import webdriver
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
    product_url_selector = None
    product_image_selector = None
    product_rating_selector = None

    def __init__(self, store_url:str = None, query_url:str = None, product_card_elem:dict = None) -> None:
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

    def search_product(self, query):
        """Search for a product in the shopping site using a query.
        Returns a list of products found and their attributes
        """
        query = "+".join(query.split(' '))
        search_url = f"{self.query_url}{query}"
        # Seacrh for product
        self.driver.get(search_url)
        # Wait to load
        print('product card', self.product_card_selector)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.product_card_selector)))
        
        # Safe wait
        WebDriverWait(self.driver, 2)
        # amazon product card = puis-card-container s-card-container s-overflow-hidden aok-relative puis-expand-height puis-include-content-margin puis puis-v3t0ujb76xyein1zb6jmoprqycb s-latency-cf-section puis-expand-last-child puis-card-border
        # amazon product title = a-size-small a-color-base a-text-normal
        # amazon product url = a-link-normal s-faceout-link a-text-normal
        # amazon image class = s-image
        # amazon rating class = a-size-mini
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
                # 'product_rating': product_card.find_element(By.CSS_SELECTOR, self.product_rating_selector).text
            })
        return products


