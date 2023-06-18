from datetime import datetime
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup


class ScraperAmazon:
    def __init__(self, books_list):
        self.books_list = books_list
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64)"
                "AppleWebKit/537.36 (KHTML, like Gecko)"
                "Chrome/44.0.2403.157 Safari/536.36"
            ),
            "Accept-Language": "en-US, en;q=0.5",
        }

    def get_products_urls(self):
        """
        Return a list of URLs.

        """

        urls_list = []
        for book in self.books_list:
            url = f"https://www.amazon.com.br/dp/{book}/"
            urls_list.append(url)
        return urls_list

    def get_products_info(self):
        """
        Return a list containing title, description, rating and price of the product.

        """

        list_books_urls = self.get_products_urls()
        product_title_list = []
        product_description_list = []
        product_rating_list = []
        product_price_list = []

        for book_url in list_books_urls:
            response = requests.get(book_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            product_title = soup.find("span", attrs={"id": "productTitle"}).text.strip()
            product_description = soup.find(
                "div", attrs={"class": "a-section a-spacing-small a-padding-small"}
            ).text.strip()
            product_rating = soup.find(
                "span", attrs={"class": "a-icon-alt"}
            ).text.strip()
            product_price = soup.find(
                "div",
                attrs={
                    "class": "a-section aok-hidden twister-plus-buying-options-price-data"
                },
            ).text.split(", ")

            for price in product_price:
                price_dict = json.loads(price)
                price_amount = price_dict[0]["priceAmount"]

            product_title_list.append(product_title)
            product_description_list.append(product_description)
            product_rating_list.append(product_rating)
            product_price_list.append(price_amount)

            all_products_info = [
                {
                    "book_title": item1,
                    "book_description": item2,
                    "book_rating": item3,
                    "book_price": item4,
                }
                for item1, item2, item3, item4 in zip(
                    product_title_list,
                    product_description_list,
                    product_rating_list,
                    product_price_list,
                )
            ]
        return all_products_info

    def transform_data_to_dataframe(self):
        """
        Return a dataframe containing the products information.

        """

        df = pd.DataFrame(self.get_products_info())
        df["date"] = datetime.now().date()
        return df
