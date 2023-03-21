from random import randint
import requests
from decouple import config
import json

from constants import TELEGRAM_API_URL, AEROFLOT_API_URL

DEBUG = config("DEBUG", default=False, cast=bool)
TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN", default="hehe, hack me!", cast=str)
TELEGRAM_CHANNEL = config("TELEGRAM_CHANNEL", default="hehe, hack me again!", cast=int)


def get_data(direction='to'):
    data = {}
    if direction == 'to':
        data = {
            "program_id": 40,
            "routes": [
                {
                    "origin": "MOW",
                    "destination": "LED",
                    "departure_date": "2023-04-06"
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
    elif direction == 'from':
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

    headers = {
        'User-Agent': 'PostmanRuntime/7.31.3',
        'Content-Type': 'application/json;charset=utf-8'
    }
    response = requests.post(AEROFLOT_API_URL, data=json.dumps(data), headers=headers)

    return response.json()


def generate_markdown(data, direction):
    direction_to_text = {
        'to': 'туда',
        'from': 'обратно',
    }
    if data['success']:
        data = data['data']
        if data['route_min_prices']:
            return f'*Есть билеты {direction_to_text[direction]}*\n[Купить билет](https://www.aeroflot.ru/sb/subsidized/app/ru-ru#/search?_k=kq1xey)'
        else:
            return f'Билетов {direction_to_text[direction]} всё еще нет :('
    return f'Запрос на получение билетов {direction_to_text[direction]} не удался :(\n\n\n{data}'


def send_message(text):
    url = f"{TELEGRAM_API_URL}{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHANNEL,
        "text": text,
        "parse_mode": "markdown",
    }
    return requests.post(url, data=data).json()


def check_tickets(direction='to'):
    data = get_data(direction)
    if data['data']['route_min_prices'] or randint(1, 24) == 1 or DEBUG:
        markdown = generate_markdown(data, direction)
        send_message(markdown)


if __name__ == '__main__':
    check_tickets()
    check_tickets('from')
