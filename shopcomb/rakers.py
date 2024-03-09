"""Scraper for specific sites"""
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from shopcomb.shopcomb import Shopcomb

class AmazonRaker(Shopcomb):
    """Scraper for Amazon shopping site"""
    store_url = "https://www.amazon.com"
    query_url = "https://www.amazon.com/s?k="
    product_card_selector = "div.puis-card-container.s-card-container"
    product_title_selector = "span.a-color-base.a-text-normal"
    product_price_selector = "span.a-price-whole"
    product_url_selector = "h2 a.a-link-normal.a-text-normal"
    product_image_selector = "img.s-image"
    product_rating_selector = "a-size-mini"

class AliExpressRaker(Shopcomb):
    """Scraper for Aliexpress Shopping site"""
    store_url = "https://www.aliexpress.com/"
    query_url = "https://www.aliexpress.com/w/wholesale-"
    product_card_selector = "div.search-item-card-wrapper-gallery"
    product_title_selector = "h3.multi--titleText--nXeOvyr"
    product_price_selector = "div.multi--price-sale--U-S0jtj span"
    product_url_selector = "a.search-card-item"
    product_image_selector = "img.images--item--3XZa6xf"
    product_rating_selector = "a-size-mini"

    def form_search_url(self, query: str):
        query = "-".join(query.split(' '))
        search_url = f"{self.query_url}{query}.html"
        return search_url
    
    def get_price(self, product_card: WebElement):
        spans = product_card.find_elements(By.CSS_SELECTOR, self.product_price_selector)
        price_text = []
        for span in spans:
            price_text.append(span.text)
        price = ''.join(price_text)
        return price
        
