import os

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

print(print_tree('saved_image'))