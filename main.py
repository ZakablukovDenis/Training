import time
import requests
# from pprint import pprint
from tqdm import tqdm

# vk_id = input("Введите ID: ")
vk_id = 210700286

with open('token.txt', 'r') as file_object:
    vk_token = file_object.read().strip()
vk_url = 'https://api.vk.com/method/photos.get'
params = {'owner_id': vk_id, 'album_id': 'profile', 'extended': 1, 'access_token': vk_token, 'v': '5.131'}

with open('ya_token.txt', 'r') as file:
    yandex_token = file.read().strip()
yandex_url = "https://cloud-api.yandex.net/v1/disk/resources"
yandex_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'OAuth {yandex_token}'}


def upload_file(url, name):
    params_info = {'path': name, 'url': url}
    info = requests.post(f"{yandex_url}/upload", params=params_info, headers=yandex_headers)
    print(info.status_code)
    # if info.status_code == 202:
    #     print(f"Photo {name} saved")
    # else:
    #     print(f"Ошибка: {info.status_code}")


def link_photo():
    foto = requests.get(vk_url, params=params)
    print(f"STATUS CODE: {foto.status_code}")
    print("Получаем URL на объекты")
    for val in foto.json().values():
        for i in tqdm(val['items']):
            time.sleep(1)
            file_name = str(i['likes']['count']) + ".jpg"
            photo_url = i['sizes'][-1]['url']
            upload_file(photo_url, f"{vk_id}/{file_name}")


def create_directory(name_dir):
    rez = requests.put(f'{yandex_url}?path={name_dir}', headers=yandex_headers)
    if rez.status_code == 201:
        print(f"Каталог '{name_dir}' создан")
    else:
        print(f"Error {rez.status_code}")


if __name__ == '__main__':
    create_directory(vk_id)
    link_photo()
