import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent as ua
from decimal import Decimal

headers = {
    'authority': 'www.bestchange.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': ua().random
}


def tokens():
    dct = {}
    response = requests.get('https://www.bestchange.com/', headers=headers)
    bs = BeautifulSoup(response.text, 'lxml')
    search = bs.find('select', id='currency_lc').find('optgroup', class_='bgw').find_all('option')
    for item in search:
        temp = item.text.split('(')
        temp[1] = temp[1][:-1]
        dct[temp[0].strip()] = '-'.join(temp[0].strip().lower().split())
    return dct


def exchange_full_info(give='Tether TRC20', get='Bitcoin'):
    exchange = f'https://www.bestchange.com/{give}-to-{get}.html'
    response_ex = requests.get(exchange, headers=headers)
    bs_ex = BeautifulSoup(response_ex.text, 'lxml')
    exchangers_info = []
    upk = {}
    for item in bs_ex.find('table', id='content_table').find('tbody').find_all('tr'):
        upk['Exchanger name'] = item.find('td', class_='bj').find('div', class_='pc').text
        try:
            upk['Exchanger info'] = item.find('td', class_='bj').find('span', class_='lbpl').text.split('.')[:-1]
        except AttributeError:
            upk['Exchanger info'] = ''
        upk['You will give'] = item.find('td', class_='bi').find('div', class_='fs').text
        upk['You will get'] = item.find_all('td')[3].text
        upk['Amount range'] = [i.text for i in item.find('td', class_='bi').find('div', class_='fm').find_all('div')]
        upk['Exchanger reserve'] = item.find_all('td')[4].text
        upk['Feedback'] = item.find_all('td')[5].text

        exchangers_info.append(upk)
        upk = {}
    return exchangers_info


def exchangers_best_cost(give='Tether TRC20', get='Bitcoin'):
    exchange = f'https://www.bestchange.com/{give}-to-{get}.html'
    temp = f'{exchange_full_info(exchange)[0]["You will give"]}\n{exchange_full_info(exchange)[0]}'
    return temp


def exchange_all_costs(give='Tether TRC20', get='Bitcoin'):
    exchange = f'https://www.bestchange.com/{give}-to-{get}.html'
    return [item['You will give'] for item in exchange_full_info(exchange)]


def find_exchanger_by_name(name: str, give='Tether TRC20', get='Bitcoin'):
    exchange = f'https://www.bestchange.com/{give}-to-{get}.html'
    for item in exchange_full_info(exchange):
        temp = item['Exchanger name'].lower()
        if temp == name.lower() or temp in name.lower() or name.lower() in temp:
            return item


def find_exchanger_by_reserve(num: int, give='Tether TRC20', get='Bitcoin'):
    exchange = f'https://www.bestchange.com/{give}-to-{get}.html'
    lst = []
    for item in exchange_full_info(exchange):
        if Decimal(item['Exchanger reserve'].strip()) >= num:
            lst.append(item)

    lst.sort(key=lambda x: Decimal(x['Exchanger reserve'].strip()), reverse=True)
    return lst


def find_exchanger_by_feedback_count(num: int, give='Tether TRC20', get='Bitcoin'):
    exchange = f'https://www.bestchange.com/{give}-to-{get}.html'
    lst = []
    for item in exchange_full_info(exchange):
        if int(item['Feedback'].strip()) >= num:
            lst.append(item)

    lst.sort(key=lambda x: int(x['Feedback'].strip()), reverse=True)
    return lst


def find_exchanger_by_amount(num: int, give='Tether TRC20', get='Bitcoin'):
    exchange = f'https://www.bestchange.com/{give}-to-{get}.html'
    lst = []
    for item in exchange_full_info(exchange):
        min_amount = Decimal(''.join(item['Amount range'][0].split()[1:]))
        max_amount = Decimal(''.join(item['Amount range'][1].split()[1:]))
        if min_amount <= num <= max_amount:
            lst.append(item)

    return lst

