import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def is_shorten_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == "vk.cc"


def createParser():
    parser = argparse.ArgumentParser(
        description='Описание что делает программа'
    )
    parser.add_argument('url', help='Введите url')
    args = parser.parse_args()
    return args.url


def count_clicks(token, link, vk_user_id):
    parsed_url = urlparse(link)
    parsed_url_path = parsed_url.path.replace("/", "")
    payload = {
        "access_token": token,
        "key": parsed_url_path,
        "user_id": vk_user_id,
        "v": "5.131",
        "interval": "forever",
    }
    url = "https://api.vk.ru/method/utils.getLinkStats"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response = response.json()
    if response["response"]["stats"]:
        click = response["response"]["stats"][0]["views"]
    else:
        click = 0
    return click


def shorten_link(token, url, vk_user_id):
    payload = {
        "url": url,
        "user_id": vk_user_id,
        "v": "5.131",
        "access_token": token,
    }
    url = "https://api.vk.ru/method/utils.getShortLink"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    short_link = response.json()["response"]["short_url"]
    return short_link


if __name__ == "__main__":
    url = createParser()
    load_dotenv()
    vk_token = os.getenv("VK_API_KEY")
    vk_user_id = os.getenv("VK_USER_ID")
    try:
        user_input = url
        if is_shorten_link(user_input):
            print(f"По вышей ссылке перешли {count_clicks(vk_token, user_input, vk_user_id)} раз")
        else:
            print(shorten_link(vk_token, user_input, vk_user_id))
    except requests.exceptions.HTTPError:
        print("Некорректный url")
