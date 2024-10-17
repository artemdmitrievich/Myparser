# in venv:
# python -m pip install requests, BeautifulSoup4
# if not work:
# py -m pip install requests, BeautifulSoup4

import requests
from bs4 import BeautifulSoup
from time import time, sleep
from urllib.parse import urljoin

headers = {"User-Agent": 
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"}

url = "https://www.coingecko.com/ru"
responce = requests.get(url, headers=headers)
soup = BeautifulSoup(responce.text, 'lxml')

data_market_capitalization = soup.find("div", class_="tw-font-bold tw-text-gray-900 dark:tw-text-moon-50 tw-text-lg tw-leading-7").text
print(data_market_capitalization)

change_market_capitalization_value = soup.find("span", class_="gecko-down").text

url_global_charts = "https://www.coingecko.com/ru/global-charts"
responce_global_charts = requests.get(url_global_charts, headers=headers)
soup_global_charts = BeautifulSoup(responce_global_charts.text, "lxml")

url_css = "https://static.coingecko.com/packs/css/v2/application-c86563d7.chunk.css"
responce_url = requests.get(url_css, headers=headers)
soup_css = str(BeautifulSoup(responce_url.text, "lxml"))
decrease_in_capitalization = '.gecko-down{--tw-text-opacity:1;color:rgb(255 58 51'

def change_market_capitalization():
    if decrease_in_capitalization in soup_css:
        return f'Рыночная капитализация снизилась на {change_market_capitalization_value}'
    else:
        return f'Рыночная капитализация увеличилась на {change_market_capitalization_value}'

print(change_market_capitalization())
