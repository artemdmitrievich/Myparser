import requests
from bs4 import BeautifulSoup
from static.headers import Headers


url = "https://www.coingecko.com/ru"
responce = requests.get(url, headers=Headers)
soup = BeautifulSoup(responce.text, "lxml")