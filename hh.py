# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов Superjob и HH.
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# ● Наименование вакансии.
# ● Предлагаемую зарплату (отдельно минимальную и максимальную).
# ● Ссылку на саму вакансию.
# ● Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import json
from time import sleep


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
occupation = 'аналитик'
main_link = 'https://hh.ru'
response = requests.get(f'{main_link}/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text={occupation}', headers=headers).text
soup = bs(response,'lxml')
pages = soup.find_all('a', {'class': 'bloko-button HH-Pager-Control'})
print(int(pages[-1].text))
hh_vac_parce_list = []

for page in range(int(pages[-1].text)):
    link = f'{main_link}/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text={occupation}&page={page}'
    response = requests.get(link, headers=headers).text
    soup = bs(response, 'lxml')
    hh_vac_block = soup.find_all('div', {'class': 'vacancy-serp'})
    hh_vac_list = hh_vac_block[0].find_all('div', {'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_premium'}) + \
                  hh_vac_block[0].find_all('div', {'data-qa': 'vacancy-serp__vacancy'})
    for i in hh_vac_list:
        dict = {}
        if not i.find_all('a', {'class': 'bloko-link HH-LinkModifier'}):
            dict['name'] = None
            dict['link'] = None
        else:
            dict['name'] = i.find_all('a', {'class': 'bloko-link HH-LinkModifier'})[0].text
            dict['link'] = i.find_all('a', {'class': 'bloko-link HH-LinkModifier'})[0]['href']
        if not i.find_all('a', {'data-qa': 'vacancy-serp__vacancy-employer'}):
            dict['employer'] = None
        else:
            dict['employer'] = i.find_all('a', {'data-qa': 'vacancy-serp__vacancy-employer'})[0].text
        sal = i.find_all('span', {'class': 'bloko-section-header-3 bloko-section-header-3_lite'})
        if len(sal) == 1:
            dict['sal_min'] = None
            dict['sal_max'] = None
            dict['sal_cur'] = None
        else:
            dict['sal_min'] = ''
            dict['sal_max'] = ''
            dict['sal_cur'] = ''
            spec_sal = sal[1].text
            spec_sal = spec_sal.replace(' ', "\xa0")
            spec_sal = spec_sal.replace('-', "\xa0-\xa0")
            sal_list = spec_sal.split("\xa0")
            if 'от' in sal_list:
                for elem in sal_list[1:len(sal_list) - 1]:
                    dict['sal_min'] += elem
            elif 'до' in sal_list:
                for elem in sal_list[1:len(sal_list) - 1]:
                    dict['sal_max'] += elem
            elif '-' in sal_list:
                pos = sal_list.index('-')
                for elem in sal_list[:pos]:
                    dict['sal_min'] += elem
                for elem in sal_list[pos + 1:len(sal_list) - 1]:
                    dict['sal_max'] += elem
            else:
                for elem in sal_list[1:len(sal_list) - 1]:
                    dict['sal_min'] += elem
                    dict['sal_max'] += elem
            dict['sal_min'] = None if dict['sal_min'] == '' else dict['sal_min']
            dict['sal_max'] = None if dict['sal_max'] == '' else dict['sal_max']
            dict['sal_cur'] = None if 'По договорённости' in sal_list else sal_list[-1]
        hh_vac_parce_list.append(dict)
    sleep(0.5)
df = pd.DataFrame(hh_vac_parce_list)
print(df)
df.to_csv(f'hh_{occupation}.csv', encoding='utf-8')
with open(f'hh_{occupation}.json', 'w', encoding='utf-8') as outfile:
    json.dump(hh_vac_parce_list, outfile)
