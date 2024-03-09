"""The main program"""
import os
from pprint import pprint

from shopcomb.shopcomb import Shopcomb
from shopcomb.rakers import AmazonRaker, AliExpressRaker

def main():
    query = input("Enter search query:")
    amazon =AmazonRaker()
    pprint(amazon.search_product(query))



if __name__ == "__main__":
    # Check if 'chrome' dir exist
    if not os.path.exists(os.path.relpath('shopcomb/chrome')):
        print("Unpackage google-chrome-stable_current_amd64.deb to shopcomb/")
        print("Try running 'mkdir shopcomb/chrome'")
        print("dpkg -x google-chrome-stable_current_amd64.deb shopcomb/chrome")
        exit()
    main()

        