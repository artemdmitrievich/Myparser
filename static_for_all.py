import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

url = "https://www.coingecko.com/ru"
responce = requests.get(url, headers=headers)
soup = BeautifulSoup(responce.text, "lxml")
