#%%

from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests
import json


headers = {
    'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                    'AppleWebKit/537.36 (KHTML, like Gecko)'
                    'Chrome/44.0.2403.157 Safari/537.36'),
    'Accept-Language': 'en-US, en;q=0.5'
}

#%%

BOOKS = ['1942788339','8576082675']

def get_products_urls(books_list):
    
    urls_list = []
    for book in books_list:
        url = f"https://www.amazon.com.br/dp/{''.join(book)}/"
        urls_list.append(url)
    return urls_list

#%%

def get_products_info():
    lista = get_products_urls(BOOKS)
    productTitle = []
    productDescription = []
    productRating = []
    productPrice = []
    
    for book_url in range(0, len(lista)):
        response = requests.get(lista[book_url], headers = headers)
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
    return productTitle, productDescription, productRating, productPrice
        

#%%

def transform_data_to_dataframe():
    products_lists = list(get_products_info())
    
    df = pd.DataFrame({
    'book_title': products_lists[0],
    'book_description': products_lists[1],
    'book_rating': products_lists[2],
    'book_price': products_lists[3],
    'date': datetime.now()
    })
    
    return df

#%%
def creating_csv(path):
    df = pd.read_csv(path)
    
    if df.empty:
        return transform_data_to_dataframe().to_csv(path, index = False, sep = ',')
        
    else:
        new_df = df.append(transform_data_to_dataframe()).sort_index().reset_index(drop = True)
        return new_df.to_csv(path, index = False, sep = ',')

    

#%%

path = "path"

creating_csv(path)
