import requests
from bs4 import BeautifulSoup
from Parsers_aio.headers_aio import Headers


def coingecko_soup():
    url = "https://www.coingecko.com/ru"
    responce = requests.get(url, headers=Headers)
    soup = BeautifulSoup(responce.text, "lxml")
    return soup
