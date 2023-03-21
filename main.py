import requests
from decouple import config

from constants import TELEGRAM_API_URL

TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN", default="hehe, hack me!", cast=str)
TELEGRAM_CHANNEL = config("TELEGRAM_CHANNEL", default="hehe, hack me again!", cast=int)


def send_message(text):
    url = f"{TELEGRAM_API_URL}{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHANNEL,
        "text": text,
        "parse_mode": "markdown",
    }
    return requests.post(url, data=data).json()


if __name__ == '__main__':
    response = send_message("работает?")
    print(response)
