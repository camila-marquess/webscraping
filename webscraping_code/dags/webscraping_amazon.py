from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from utils import scraper

BOOKS = ["1942788339", "8576082675"]

with DAG(
    dag_id="webscraping_amazon_books",
    start_date=datetime.now(),
    schedule_interval="@daily",
) as dag:

    @dag.task()
    def start_process():
        process = scraper.ScraperAmazon(BOOKS)
        process.get_products_urls()
        process.get_products_info()
        process.transform_data_to_dataframe()

    start_process()
