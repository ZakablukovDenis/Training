import time
import requests
from pprint import pprint
from tqdm import tqdm

vk_id = input("Введите ID: ")
# vk_id = 210700286

with open('token.txt', 'r') as file_object:
    vk_token = file_object.read().strip()
vk_url = 'https://api.vk.com/method/photos.get'
params = {
    'owner_id': vk_id,
    'album_id': 'profile',
    'extended': 1,
    'access_token': vk_token, 'v': '5.131'
}

with open('ya_token.txt', 'r') as file:
    yandex_token = file.read().strip()
yandex_url = "https://cloud-api.yandex.net/v1/disk/resources"
yandex_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'OAuth {yandex_token}'
}

link_list = []


def find_folder():
    report = requests.get(f"{yandex_url}?path={vk_id}", headers=yandex_headers)
    return report.status_code
    # pprint(report.content.decode("utf-8"))


def upload_file(url, name):
    params_info = {
        'path': name,
        'url': url
    }
    info = requests.post(f"{yandex_url}/upload",
                         params=params_info,
                         headers=yandex_headers)
    # if info.status_code == 202:
    #     print(f"Photo {name} saved")
    # else:
    #     print(f"Ошибка: {info.status_code}")


def link_photo():
    foto = requests.get(vk_url, params=params)
    # print(f"STATUS CODE: {foto.status_code}")
    # print("Получаем URL на объекты")
    # pprint(foto.json())
    for val in foto.json().values():
        for i in tqdm(val['items'], desc='Идет загрузка фото'):
            time.sleep(0.5)
            file_name = str(i['likes']['count']) + ".jpg"
            photo_url = i['sizes'][-1]['url']
            photo_sizes = i['sizes'][-1]['type']
            # print("\n", file_name, photo_sizes)
            # print(photo_url, "\n", "="*10)
            upload_file(photo_url, f"{vk_id}/{file_name}")
            # ==================================================
            link_list.append({
                "file_name": file_name,
                "size": photo_sizes
            })
    print("Загрузка успешно завершена")


def create_directory(name_dir):
    rez = requests.put(f'{yandex_url}?path={name_dir}', headers=yandex_headers)
    if rez.status_code == 201:
        print(f"Каталог '{name_dir}' создан")
    else:
        print(f"Error {rez.status_code}")


if __name__ == '__main__':
    if find_folder() == 200:
        link_photo()
    elif find_folder() == 404:
        create_directory(vk_id)
        link_photo()