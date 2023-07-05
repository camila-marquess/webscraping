from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from utils import scraper

BOOKS = ["1942788339", "8576082675"]

with DAG(
    dag_id="webscraping_amazon_books",
    start_date=datetime.now(),
    schedule_interval="@daily",
) as dag:
    start_process = scraper.ScraperAmazon(BOOKS)
    
    get_url_list_task = PythonOperator(
        task_id='get_url_list_task',
        python_callable=start_process.get_products_url,
        dag=dag,
        provide_context=True,
    )
    
    get_products_info_task = PythonOperator(
        task_id='get_products_info_task',
        python_callable=start_process.get_products_info,
        dag=dag,
        provide_context=True,
    )
    
    transform_data_task = PythonOperator(
        task_id='transform_data_task',
        python_callable=start_process.transform_data,
        dag=dag,
        provide_context=True,
    )
    
    #     process.get_products_urls()
    #     process.get_products_info()
    #     process.transform_data_to_dataframe()
    #     #process.teste()

    # start_process()
    
    get_url_list_task >> get_products_info_task >> transform_data_task
