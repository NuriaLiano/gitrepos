from colorama import Fore, Style, init
import gitlab, os, shutil
import requests
import utils
init(autoreset=True, convert=True)

def remove_github(repo_name, gh_api_url, gh_token, gh_username, org_name=None):
    headers = {
        "Authorization": f"Token {gh_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    #build url 
    if org_name:
        gh_project_url = gh_api_url + org_name + "/" + repo_name
    else:
        gh_project_url = gh_api_url + gh_username + "/" + repo_name

    response = requests.delete(gh_project_url, headers=headers)

    if response.status_code == 204:
        print(Fore.GREEN + f'[SUCCESS - GITHUB DELETE] {repo_name} deleted successfully')
    else:
        print(Fore.RED + f'[ERROR] {repo_name} failed to delete Github repository')
        print(Fore.RED + f'[ERROR] response {response.json()}')

def remove_gitlab(repo_name, gl_url, gl_token):
    instance = utils.open_gitlab_instance(gl_url, gl_token)
    #check if repo exists
    gl_id_repo = utils.get_gitlab_id_repo(instance, repo_name)
    if gl_id_repo is None:
        print(Fore.YELLOW + f'[WARNING] {repo_name} does not exist.')
        return None

    try:
        # Eliminar el repositorio
        instance.projects.delete(gl_id_repo)
        print(Fore.GREEN + f'[SUCCESS - GITLAB DELETED] {repo_name} in GITLAB has been deleted successfully')
    except gitlab.exceptions.GitlabDeleteError as e:
        print(Fore.RED + f'[ERROR] Failed to delete {repo_name} in GITLAB: {e}')

def remove_local(main_path, repo_name):
    local_path = main_path + repo_name
    try:
        if os.path.exists(local_path):
            shutil.rmtree(local_path)
            print(Fore.GREEN + f'[SUCCESS - LOCAL DELETED] {local_path} has been deleted')
    except Exception as e:
        print(Fore.RED + f'[ERROR] {e}')