import os
import json
from datetime import datetime

def list_files(dir):
    dir_tree = {}
    for root, subdirs, files in os.walk(dir): #percorre o diretório
        for subdir in subdirs:
            full_path = os.path.join(root, subdir) #une o subdiretório à raiz
            dir_tree[subdir] = []
            for file_name in os.listdir(full_path): #retorna lista com nomes de entrada no subdiretório
                if os.path.isfile(os.path.join(full_path, file_name)):
                    name, extension = os.path.splitext(file_name)
                    dir_tree[subdir].append({'name': name, 'extension': extension})
    return dir_tree
directory_path = input("Enter the file path:")
if not os.path.isdir(directory_path):
  print('The given path is not a valid directory.')
else:
  dir_tree = list_files(directory_path)
  file_name = input("Enter the file name (with its extension):")
  if not file_name:
    now = datetime.now()
    file_name = f"{now.strftime('%Y_%m_%d_%H_%M_%S')}_{os.path.basename(directory_path)}.json"
    print(f"File not found")
  file_path = os.path.join('..', 'public', 'data', file_name)
  with open(file_path, 'w') as json_file:
    json.dump(dir_tree, json_file, indent=4) #parâmetro opcional nomeado
  print(f"Data saved with success in file '{file_name}'")