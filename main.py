import requests
from tqdm import tqdm
import json
import os
import math

def scrap_pixels(query=''):
    headers = {"Authorization":'GYBqxg0fR6O2aJ62dILiMDn48x5frUyz56zCnjrhgZyfjs7EgqcAgUEy'}
    query_str = f'https://api.pexels.com/v1/search?query={query}&per_page=80&orientation=landscape'

    # proxies ={
    #     'https': f'http://{os.getenv("LOGIN")}:{os.getenv("PASSWORD")}@217.29.53.133:10166'
    # }

    response = requests.get(url=query_str,headers=headers)

    if response.status_code !=200:
        return f'Ощибка: Статус код {response.status_code}, {response.json()}'
    
    img_dir_path = '_'.join(i for i in query.split(' ') if i.isalnum())

    if not os.path.exists(img_dir_path):
        os.makedirs(img_dir_path)

    json_data = response.json()

    with open(f'result_{query}.json','w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)

    images_count = json_data.get('total_results')

    if not json_data.get('next_page'):
        img_urls = [item.get('src').get('original') for item in json_data.get('photos')]
        download_images(img_list=img_urls,img_dir_path=img_dir_path)
    else:
        print(f'[INFO] Всего изображений:{images_count}.Сохранение займет какоето время')

        images_list_urls = []

        for page in range(1, math.ceil(images_count/80)+1):
            query_str = f'{query_str}&page={page}'
            response = requests.get(url=query_str, headers=headers)
            json_data = response.json()
            img_urls = [item.get('src').get('original') for item in json_data.get('photos')]
            images_list_urls.extend(img_urls)
        download_images(img_list=images_list_urls, img_dir_path=img_dir_path)

def download_images(img_list=[], img_dir_path=''):
    for item_url in tqdm(img_list):
        response = requests.get(url=item_url)

        if response.status_code == 200:
            with open(f'./{img_dir_path}/{item_url.split("-")[-1]}','wb') as file:
                file.write(response.content)
        else:
            print('Чтото пошло не по плану!(')

    # print(img_dir_path)
    # print(response.json())

def main():
    query = input('Введите ключивую фразу для поиска: ')
    scrap_pixels(query=query)

if __name__=="__main__":
    main()