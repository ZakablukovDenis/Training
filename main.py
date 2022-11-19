# import time

import requests
from pprint import pprint

# vk_id = input("Введите ID: ")
vk_id = 210700286
with open('ya_token.txt', 'r') as file:
    yandex_token = file.read().strip()
yandex_url = "https://cloud-api.yandex.net/v1/disk/resources"
yandex_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'OAuth {yandex_token}'}


def upload_file():
    url_foto = 'https://sun9-26.userapi.com/impg/TxEGuOepxRDkWhCrl2q6DyWsYb1SUTe6U0TnMg/JXNhJfWH-aw.jpg' \
               '?size=510x765' \
               '&quality=95' \
               '&sign=d33bbe431841f45147038521e419cf7d' \
               '&c_uniq_tag=JqAFRUie2ORX8uOwdg8TNbFJnXfecJ05ljmXM79Vymk' \
               '&type=album'

    info = requests.post(f"{yandex_url}/upload?path=Test_name&url={url_foto}", headers=yandex_headers)
    print(info.status_code)
    pprint(info.json())


def link_photo():
    with open('token.txt', 'r') as file_object:
        vk_token = file_object.read().strip()
    vk_url = 'https://api.vk.com/method/photos.get'
    params = {'owner_id': vk_id, 'album_id': 'profile', 'extended': 1, 'access_token': vk_token, 'v': '5.131'}
    res = requests.get(vk_url, params=params)
    print(res.status_code)
    # pprint(res.json())
    for val in res.json().values():
        for i in val['items']:
            file_name = i['likes']['count']
            photo_url = i['sizes'][-1]['url']
            print(file_name)
            print(photo_url)


def create_directory():
    name_dir = input("Введите имя каталога:")
    rez = requests.put(f'{yandex_url}?path={name_dir}', headers=yandex_headers)
    # print(rez.status_code)
    if rez.status_code == 201:
        print(f"Каталог '{name_dir}' создан")
    else:
        print(f"Error {rez.status_code}")


if __name__ == '__main__':
    link_photo()
    upload_file()
