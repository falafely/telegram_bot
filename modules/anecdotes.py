from bs4 import BeautifulSoup as bs
import requests


URL = 'https://ru.investing.com/crypto/'

r = requests.get(URL)

soap = bs(r.text, 'html.parser')

anec = soap.find('div', class_='cryptocurrency-table-block')
