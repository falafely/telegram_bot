from bs4 import BeautifulSoup as bs
import requests

URL = 'https://www.vbr.ru/crypto/'
U_A = 'Mozilla/5.0 (X11; Linux x86_64) ' \
      'AppleWebKit/537.36 (KHTML, like Gecko) ' \
      'Chrome/114.0.0.0 Safari/537.36'
headers = {'User-Agent': U_A}

page = requests.get(URL, headers=headers)

soup = bs(page.content, 'html.parser')


def btc():
    BTC = soup.find('td', {'class': 'rates-val', 'data-col': 'Rub'}).find('div', {'class': 'rates-calc-block -big-sum'})
    return BTC.text


# def eth():
#     ETH = soup.find('td', {'class': 'rates-val', 'data-col': 'Rub'}).find('div', {'class': 'rates-calc-block -big-sum'})
#     return ETH.text
