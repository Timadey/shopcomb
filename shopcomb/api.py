from fastapi import FastAPI, Query
import json  # Import the json library
from typing import Optional
import pantab as pt

from alibaba import scrape_aliexpress  # Import the function from alibaba.py
from amazon import scrape_amazon  # Import the scraping function
from hyper import dataframe_to_hyper


app = FastAPI()

@app.get("/scrape")
async def scrape_products(search_term: str = Query(..., description="The product to search for"),
                           num_pages: int = Query(5, description="Number of pages to scrape")):
    
    """Scrapes product data from Amazon for the given search term.

    Args:
        search_param (str): The product to search for on Amazon.
        number_of_pages (int, optional): Number of pages to scrape (default: 5, minimum: 1).

    Returns:
        dict: An hyper file path containing scraped product to be used in tableau for further analysis
    """
    df = scrape_aliexpress(search_term, num_pages)

    hyper_file = dataframe_to_hyper(df, f'{search_term} aliexpress.hyper')

    return hyper_file

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
        dict: An hyper file path containing scraped product to be used in tableau for further analysis

    Raises:
        ValueError: If the number of pages is less than 1.
    """

    if number_of_pages < 1:
        raise ValueError("Number of pages must be at least 1.")

    try:
        df = scrape_amazon(search_param, number_of_pages)
        hyper_file = dataframe_to_hyper(df, f'{search_param} amazon.hyper')
        return hyper_file
    except Exception as e:
        return {"error": str(e)}  # Handle potential scraping errors