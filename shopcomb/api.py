from fastapi import FastAPI, Query
from alibaba import scrape_aliexpress  # Import the function from alibaba.py

app = FastAPI()

@app.get("/scrape")
async def scrape_products(search_term: str = Query(..., description="The product to search for"),
                           num_pages: int = Query(5, description="Number of pages to scrape")):
    """Scrape product data from AliExpress for the given search term."""

    df = scrape_aliexpress(search_term, num_pages)
    return df.to_json(orient="records")  # Return results as JSON
