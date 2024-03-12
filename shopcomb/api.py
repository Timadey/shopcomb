from fastapi import FastAPI, Query
import json  # Import the json library
from typing import Optional
from alibaba import scrape_aliexpress  # Import the function from alibaba.py
from amazon import scrape_amazon  # Import your scraping function

app = FastAPI()

@app.get("/scrape")
async def scrape_products(search_term: str = Query(..., description="The product to search for"),
                           num_pages: int = Query(5, description="Number of pages to scrape")):
    """Scrape product data from AliExpress for the given search term.

    Args:
        search_term (str): This is the item that you want to search for
        number of pages (int, optional): This is the number of pages that you want to scrape data from

    Returns:
        dict: A dictionary containing scraped product data as a DataFrame (pretty-formatted JSON).    
    """

    df = scrape_aliexpress(search_term, num_pages)

    # Pretty-format the JSON output using json.dumps
    pretty_json = json.dumps(df.to_dict(orient="records"), indent=4)  # Convert DataFrame to dictionary and format

    return pretty_json  # Return the formatted JSON string


@app.get("/scrape-amazon")
async def scrape_amazon_products(
    search_param: str = Query(..., description="The product to search for on Amazon"),
    number_of_pages: Optional[int] = Query(5, gt=0, description="Number of pages to scrape (default: 5, minimum: 1)"),
):
    """Scrapes product data from Amazon for the given search term.

    Args:
        search_param (str): The product to search for on Amazon.
        number_of_pages (int, optional): Number of pages to scrape (default: 5, minimum: 1).

    Returns:
        dict: A dictionary containing scraped product data as a DataFrame (pretty-formatted JSON).

    Raises:
        ValueError: If the number of pages is less than 1.
    """

    if number_of_pages < 1:
        raise ValueError("Number of pages must be at least 1.")

    try:
        df = scrape_amazon(search_param, number_of_pages)
    except Exception as e:
        return {"error": str(e)}  # Handle potential scraping errors

    # Convert DataFrame to dictionary with records
    data_dict = df.to_dict(orient="records")

    # Pretty-format the JSON output using json.dumps with indentation
    pretty_json = json.dumps(data_dict, indent=4)  # Adjust indentation as needed

    return pretty_json  # Return the formatted JSON string
