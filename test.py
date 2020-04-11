# Изучить список открытых API.
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию.
# Ответ сервера записать в файл.

import requests
import json
from pprint import pprint

url = 'https://geocode-maps.yandex.ru/1.x/'
#headers = {'User-Agent':'Mozilla Firefox 36 (Win 8.1 x64): Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}

geocode = input('Введите адрес или координаты: ')
#geocode = 'Москва, улица Новый Арбат, дом 24'

apikey = input('Введите apikey: ')

format = 'json'

#response = requests.get(url, auth=(format, geocode, apikey), headers=headers)
response = requests.get(f'{url}?format={format}&apikey={apikey}&geocode={geocode})')

if response.ok:
    data = json.loads(response.text)
    with open(f'Geo_repos_{geocode}.json','w', encoding = 'utf-8') as outfile:
        json.dump(data, outfile)
    pprint(response.text)