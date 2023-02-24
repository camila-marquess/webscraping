
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests
import json

class ScraperAmazon:
    
    def __init__(self, books_list, path):
        self.books_list = books_list
        self.path = path
        self.headers = {
            'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                            'AppleWebKit/537.36 (KHTML, like Gecko)'
                            'Chrome/44.0.2403.157 Safari/536.36'),
            'Accept-Language': 'en-US, en;q=0.5'
        }

    def get_products_urls(self):
        urls_list = []
        for book in self.books_list:
            url = f"https://www.amazon.com.br/dp/{''.join(book)}/"
            urls_list.append(url)
        return urls_list
    
    def get_products_info(self):
        list_books_urls = self.get_products_urls()
        productTitle = []
        productDescription = []
        productRating = []
        productPrice = []
        
        for book_url in range(0, len(list_books_urls)):
            response = requests.get(list_books_urls[book_url], headers = self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
        
            product_title = soup.find("span", attrs={"id":'productTitle'}).text.strip()
            product_description = soup.find("div", attrs={"class":"a-section a-spacing-small a-padding-small"}).text.strip()
            product_rating = soup.find("span", attrs={"class":"a-icon-alt"}).text.strip()
            product_price = soup.find("div", attrs={'class': 'a-section aok-hidden twister-plus-buying-options-price-data'}).text.split(", ")
            
            for price in product_price:
                price_dict = json.loads(price) 
                price_amount = price_dict[0]['priceAmount']
                
        
            productTitle.append(product_title)
            productDescription.append(product_description)
            productRating.append(product_rating)
            productPrice.append(price_amount)
            
            dict_products = [{'book_title': item1, 'book_description': item2, 'book_rating': item3, 
                                    'book_price': item4} for item1, item2, item3, item4 in 
                                zip(productTitle, productDescription, productRating, productPrice)]
            
        return dict_products


    def transform_data_to_dataframe(self):
        df = pd.DataFrame(self.get_products_info())
        df['date'] = datetime.now()   
        return df


    def creating_csv(self, is_empty):        
        
        if is_empty is True:
            return self.transform_data_to_dataframe().to_csv(self.path, index = False, sep = ',')
            
        else:
            df = pd.read_csv(self.path)
            new_df = df.append(self.transform_data_to_dataframe()).sort_index().reset_index(drop = True)
            return new_df.to_csv(self.path, index = False, sep = ',')