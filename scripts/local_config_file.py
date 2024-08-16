import os
import json
from colorama import init, Fore

init(autoreset=True)

## this part is for local repo .config file
def create_config_file(config_path):
    with open(config_path, 'w') as data_file:
        json.dump({}, data_file, indent=4)

def open_config_data(config_path):
    try:
        with open(config_path, 'r') as data_file:
            return json.load(data_file)
    except FileNotFoundError:
        print(Fore.RED + f'[ERROR] {config_path} not found')

def add_data_to_config(key, value, config_path):
    data = open_config_data(config_path)
    data[key] = value
    try:
        with open(config_path, 'w') as data_file:
            json.dump(data, data_file, indent=4)
    except IOError:
        print(Fore.RED + f'[ERROR] something went wrong in saving data on {config_path}')