from colorama import init, Fore
import subprocess

from config import open_config_data

init(autoreset=True)

def get_gitConfig(config_key):
    command = ['git', 'config', '--get', config_key]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return None

def check_container_data(container_path_config):
    config_data = open_config_data(container_path_config)
    required_keys = ['EMAIL', 'GL_USERNAME', 'GL_TOKEN', 'GL_URL', 'GH_USERNAME', 'GH_TOKEN', 'GH_URL', 'GH_URL_REMOVE']
    if all(key in config_data for key in required_keys):
        print(Fore.GREEN + f'[SUCCESS - CHECK CONTAINER CONFIG] {container_path_config} loaded successfully')
        return True
    else:
        return False
