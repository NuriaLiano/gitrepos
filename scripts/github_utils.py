import os
import requests
from colorama import init, Fore
from config import open_config_data, add_data_to_config
from git_utils import create_path

init(autoreset=True)

def create_github_repo(gh_remove_url, gh_url, gh_url_general, gh_token, gh_username, repo_name, visibility, local_path_config):
    gh_project_url = gh_remove_url + gh_username + '/' + repo_name
    gh_repo_url = gh_url_general + gh_username + '/' + repo_name
    headers = {
        "Authorization": f"Bearer {gh_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "private": False if visibility == "public" else True
    }
    response = requests.post(gh_url, headers=headers, json=data)
    if response.status_code == 201:
        add_data_to_config('GH_PROJECT_URL', gh_project_url, local_path_config)
        add_data_to_config('GH_REPO_URL', gh_repo_url, local_path_config)
        print(Fore.GREEN + f'[SUCCESS - GITHUB CREATED] {repo_name} created successfully')
        print(Fore.CYAN + f'[CHECK] Go to {gh_project_url} to check it!')
    else:
        print(Fore.RED + f'[ERROR] {gh_project_url} failed to create Github repository')
        print(Fore.RED + f'[ERROR] response {response.json()}')

def create_path(*args):
    return os.path.join(*args)

def remove_github(repo_name, container_path, container_path_config):
    local_path_config = create_path(container_path, repo_name, ".config.json")
    gh_project_url = open_config_data(local_path_config)['GH_PROJECT_URL']
    gh_token = open_config_data(container_path_config)['GH_TOKEN']
    gh_remove_url = open_config_data(container_path_config)['GH_URL_REMOVE']
    gh_username = open_config_data(container_path_config)['GH_USERNAME']

    headers = {
        "Authorization": f"Token {gh_token}"
    }

    if gh_project_url == "":
        gh_project_url = create_path(gh_remove_url, gh_username, repo_name)
    
    response = requests.delete(gh_project_url, headers=headers)

    if response.status_code == 204:
        print(Fore.GREEN + f'[SUCCESS - GITHUB DELETE] {gh_project_url} deleted successfully')
    else:
        print(Fore.RED + f'[ERROR] {gh_project_url} failed to delete Github repository')
        print(Fore.RED + f'[ERROR] response {response.json()}')
