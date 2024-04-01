import requests
import os
import random
import shutil

def getpic(pid,config):
    fix=config['pixiv']['fix']
    geshi=config['pixiv']["img_format"]
    image_url = f'https://pixiv.{fix}/{pid}-1.{geshi}'
    r = requests.get(image_url)

    if '這個作品可能已被刪除，或無法取得' in r.text:
        return -1
    

    elif '指定' in r.text:
        image_url = f'https://pixiv.{fix}/{pid}.{geshi}'
        print(image_url)
        r = requests.get(image_url)
        os.makedirs(f'./saved_image', exist_ok=True)
        with open(f'./saved_image/{pid}.{geshi}', 'wb') as f:
            f.write(r.content)
        return 1
    

    else:
        for i in range(1, 999):
            os.makedirs(f'./saved_image/{pid}', exist_ok=True)
            image_url = f'https://pixiv.{fix}/{pid}-{i}.{geshi}'
            print(image_url)
            r = requests.get(image_url)
            if '作品' in r.text:
                return 2
            with open(f'./saved_image/{pid}/{i}.{geshi}', 'wb') as f:
                f.write(r.content)
            

def init_img_folder(img_path):
    if not os.path.exists(f"{img_path}"):
        os.makedirs(f'./{img_path}')


def random_Image():
    imgList=os.listdir("saved_image")
    img=random.choice(imgList)
    if '.' not in img:
        return random_Image()
    else:
        print(img)
        return img
    
def print_tree(path):
    file_list=os.listdir(path)
    msgstr=''
    for i in file_list:
        singepath=os.path.join(path,i)
        if os.path.isdir(singepath):
            msgstr=f'/{i}\n'+msgstr
        elif os.path.isfile(singepath):
            msgstr+=f'{i}\n'
    return msgstr

def del_img(code_name):
    for i in os.listdir('saved_image'):
        if code_name in i:
            file_name=os.path.join('saved_image',i)
            if '.' not in file_name:
                shutil.rmtree(file_name)
            else:
                os.remove(file_name)
            return True
    return False