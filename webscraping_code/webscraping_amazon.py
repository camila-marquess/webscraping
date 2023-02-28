from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from scraper import ScraperAmazon

BOOKS = ['1942788339','8576082675']
PATH = ''

def start_process():
    scraper = ScraperAmazon(BOOKS, PATH)
    scraper.get_products_urls()
    scraper.get_products_info()
    scraper.transform_data_to_dataframe()
    scraper.creating_csv(False)

def read_dataframe():
    scraper = start_process()
    
    df = pd.read_csv(PATH)
    
    return df.head()

read_dataframe()
