import pandas as pd
import re

def clean_alibaba(df):
    # Remove 'NGN' and comma from price and convert to float
    def clean_price(price):
        cleaned_price = price.replace('NGN', '').replace(',', '')
        return float(cleaned_price)

    
    # Clean shipping fee column
    def clean_shipping_fee(shipping_fee):
        if shipping_fee == 'Free shipping':
            return 0.0
        elif '+Shipping' in shipping_fee:
            # Extracting the price from the string using regular expression
            price_match = re.search(r'NGN([\d,]+\.\d+)', shipping_fee)
            if price_match:
                return float(price_match.group(1).replace(',', ''))
        else:
            return None
    
    df["Shipping Prices"] = df["Shipping Prices"].apply(clean_shipping_fee)
    df['Prices'] = df['Prices'].apply(clean_price)
    
    return df
