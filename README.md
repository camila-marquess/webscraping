# Webscraping Amazon Website

<img src="https://img.shields.io/badge/beautiulsoup-4.11.1-blue"/> <img src="https://img.shields.io/badge/python-3.10.2-blue"/> <img src="https://img.shields.io/badge/airflow-2.5.1-blue">

## 1. Description

This project was constructed in order to get products informations like price and product description from amazon website using scraping. There is a class `ScraperAmazon` that gathers functions that will get the data we want and transform it in a pandas DataFrame. 

If you'd like to run this scraping everyday so you could, for example, compare prices based on a period, you could make use of a DAG indicating a schedule for it to run. There is also an example of a DAG in this project for it. 


## 2. What you need to know 

Amazon url structure to each product is like the URL below, so what you need to change in ```BOOKS``` is the product: 

```
https://www.amazon.com.br/dp/<product>/
```
You can get the product as shown below: 

![Amazon product URL example.](https://user-images.githubusercontent.com/58270725/213030095-afcc3667-f85b-4e3b-9587-8b8f80955af4.png)

## 3. Installation

You can clone this repository using the code below: 

```
git clone https://github.com/camila-marquess/webscraping.git
```

You need to install some libraries in order to use this code:

```
pip install beautifulsoup4
```
```
pip install pandas  
```
```
pip install requests
```

Before running Airflow, make sure you have installed docker in your OS. If you do not, follow this steps based on your OS: ![Installing Docker Compose](https://docs.docker.com/desktop/install/windows-install/).

In order to start Airflow you have to run: 

```
docker-compose up -d
```

Then you can visualize the Airflow UI by accessing `localhost:8080` on your browser. The default login and password are: `airflow`.

In order to stop the containers, you can run: 

```
docker-compose down
```

