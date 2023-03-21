import datetime
import time
from random import randint
import requests
from decouple import config
import json

from constants import TELEGRAM_API_URL, AEROFLOT_API_URL

DEBUG = config("DEBUG", default=False, cast=bool)
TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN", default="hehe, hack me!", cast=str)
TELEGRAM_CHANNEL = config("TELEGRAM_CHANNEL", default="hehe, hack me again!", cast=int)


def get_data(direction='msk-spb'):
    data = {}
    if direction == 'msk-spb':
        data = {
            "program_id": 40,
            "routes": [
                {
                    "origin": "MOW",
                    "destination": "LED",
                    "departure_date": "2023-05-06"
                }
            ],
            "passengers": [
                {
                    "passenger_type": "youth",
                    "quantity": 1
                }
            ],
            "lang": "ru"
        }
    elif direction == 'spb-msk':
        data = {
            "program_id": 40,
            "routes": [
                {
                    "origin": "LED",
                    "destination": "MOW",
                    "departure_date": "2023-05-09"
                }
            ],
            "passengers": [
                {
                    "passenger_type": "youth",
                    "quantity": 1
                }
            ],
            "lang": "ru"
        }
    elif direction == 'srt-msk':
        data = {
            "program_id": 40,
            "routes": [
                {
                    "origin": "RTW",
                    "destination": "MOW",
                    "departure_date": "2023-05-06"
                }
            ],
            "passengers": [
                {
                    "passenger_type": "youth",
                    "quantity": 1
                }
            ],
            "lang": "ru"
        }
    elif direction == 'msk-srt':
        data = {
            "program_id": 40,
            "routes": [
                {
                    "origin": "MOW",
                    "destination": "RTW",
                    "departure_date": "2023-05-09"
                }
            ],
            "passengers": [
                {
                    "passenger_type": "youth",
                    "quantity": 1
                }
            ],
            "lang": "ru"
        }

    headers = {
        'User-Agent': 'PostmanRuntime/7.31.3',
        'Content-Type': 'application/json;charset=utf-8'
    }
    response = requests.post(AEROFLOT_API_URL, data=json.dumps(data), headers=headers)

    return response.json()


def generate_markdown(data, direction):
    direction_to_text = {
        'msk-spb': 'Москва-Питер',
        'spb-msk': 'Питер-Москва',
        'msk-srt': 'Москва-Саратов',
        'srt-msk': 'Саратов-Москва',
    }
    if data['success']:
        data = data['data']
        if data['route_min_prices']:
            print(datetime.datetime.now(), 'есть билеты')
            return f'*Есть билеты {direction_to_text[direction]}*\n[Купить билет](https://www.aeroflot.ru/sb/subsidized/app/ru-ru#/search?_k=kq1xey)'
        else:
            print(datetime.datetime.now(), 'нет билетов')
            return f'Билетов {direction_to_text[direction]} всё еще нет :('
    print(datetime.datetime.now(), 'запрос не удался')
    return f'Запрос на получение билетов {direction_to_text[direction]} не удался :(\n\n\n{data}'


def send_message(text):
    url = f"{TELEGRAM_API_URL}{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHANNEL,
        "text": text,
        "parse_mode": "markdown",
    }
    return requests.post(url, data=data).json()


def check_tickets(direction):
    data = get_data(direction)
    if data['data']:
        if data['data']['route_min_prices'] or randint(1, 24) == 1 or DEBUG:
            markdown = generate_markdown(data, direction)
            send_message(markdown)
    else:
        print(datetime.datetime.now(), data['error'])


if __name__ == '__main__':
    while True:
        check_tickets('msk-spb')
        check_tickets('spb-msk')
        check_tickets('srt-msk')
        check_tickets('msk-srt')
        time.sleep(60 * 60)
