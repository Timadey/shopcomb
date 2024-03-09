"""Scraper for specific sites"""
from shopcomb.shopcomb import Shopcomb

class AmazonRaker(Shopcomb):
    """Scraper for Amazon shopping site"""
    store_url = "https://www.amazon.com"
    query_url = "https://www.amazon.com/s?k="
    product_card_selector = "div.puis-card-container.s-card-container"
    product_title_selector = "span.a-color-base.a-text-normal"
    product_url_selector = "h2 a.a-link-normal.a-text-normal"
    product_image_selector = "img.s-image"
    product_rating_selector = "a-size-mini"

        
