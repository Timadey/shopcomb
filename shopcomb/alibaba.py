import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

def scrape_aliexpress(search_term, num_pages=5):
    """Scrapes product information from AliExpress for the given search term.

    Args:
       search_term (str): The product to search for.
       num_pages (int, optional): The number of pages to scrape. Defaults to 5.

    Returns:
       pd.DataFrame: A DataFrame containing the scraped product data.
    """

    browser = webdriver.Chrome()  # Open a Chrome browser instance

    website = 'https://www.aliexpress.com'
    browser.get(website)  # Navigate to AliExpress
    browser.maximize_window()  # Maximize the window for better visibility

    # Find the search bar and button elements
    input_search = browser.find_element(By.CLASS_NAME, 'search--keyword--15P08Ji')
    search_button = browser.find_element(By.CLASS_NAME, 'search--submit--2VTbd-T')

    # Perform the search
    input_search.clear()
    input_search.send_keys(search_term)
    browser.execute_script("arguments[0].click();", search_button)

    # XPaths for product information elements
    product_class = "//h3[@class='multi--titleText--nXeOvyr']"
    price_class = "//div[@class='multi--price-sale--U-S0jtj']"
    shipping_class = "//span[@class='tag--text--1BSEXVh tag--textStyle--3dc7wLU multi--serviceStyle--1Z6RxQ4']"
    store_name = "//a[@class='cards--storeLink--XkKUQFS']"

    # Lists to store Scraped information
    product_descriptions = []
    prices = []
    shipping_prices = []
    store_names = []

    # Iterate through each page
    for i in range(num_pages):
       browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')  # Scroll to bottom

       # Find elements for product information on the current page
       products = browser.find_elements(By.XPATH, product_class)
       price = browser.find_elements(By.XPATH, price_class)
       shipping = browser.find_elements(By.XPATH, shipping_class)
       stores = browser.find_elements(By.XPATH, store_name)

       # Extract product information from each product
       for j in range(len(products)):
           try:
               product_descriptions.append(products[j].text)
               prices.append(price[j].text)
               shipping_prices.append(shipping[j].text)
               store_names.append(stores[j].text)
           except:
               # Handle potential errors during extraction
               pass

       # Navigate to the next page
       next_page_input = browser.find_element(By.XPATH, "//input[@aria-label='Page']")
       next_page_button = browser.find_element(By.CSS_SELECTOR, "button.comet-pagination-options-quick-jumper-button")

       next_page_input.clear()
       next_page_input.send_keys(str(i + 1))  # Send keys to navigate to the next page
       next_page_button.click()

       sleep(10)  # Wait for page to load

    # Create and return the DataFrame
    data_set = {
       'Product Description': product_descriptions,
       'Prices': prices,
       'Shipping Prices': shipping_prices,
       'Store Names': store_names
    }
    df = pd.DataFrame(data_set)
    return df