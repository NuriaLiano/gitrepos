import gitlab
from colorama import init, Fore
from config import open_config_data, add_data_to_config

init(autoreset=True)

def open_gitlab_instance(container_path_config):
    data = open_config_data(container_path_config)
    gl_url = data['GL_URL']
    gl_token = data['GL_TOKEN']
    return gitlab.Gitlab(gl_url, private_token=gl_token)

def get_gitlab_id_repo(instance, repo_name):
    try:
        all_projects = instance.projects.list(search=repo_name, owned=True)
        for repo in all_projects:
            return repo.id
    except gitlab.exceptions.GitlabGetError as e:
        print(Fore.RED + f'[ERROR] Gitlab API error: {e}')

def create_gitlab_repo(container_path_config, repo_name, local_path_config, visibility):
    instance = open_gitlab_instance(container_path_config)
    gl_repo_id = get_gitlab_id_repo(instance, repo_name)
    if gl_repo_id is None:
        gl_repo = instance.projects.create({'name': repo_name, 'visibility': visibility})
        add_data_to_config('GL_ID_REPO', gl_repo_id, local_path_config)
        add_data_to_config('GL_REPO_URL', gl_repo.http_url_to_repo, local_path_config)
        print(Fore.GREEN + f'[SUCCESS - GITLAB CREATED] {repo_name} created successfully')
        print(Fore.CYAN + f'[CHECK] Go to {gl_repo.http_url_to_repo} to check it!')
    else:
        print(Fore.RED + f'[ERROR] {repo_name} already exists')

def remove_gitlab(container_path, container_path_config, repo_name):
    instance = open_gitlab_instance(container_path_config)
    gl_id_repo = get_gitlab_id_repo(instance, repo_name)
    if gl_id_repo is not None:
        instance.projects.delete(gl_id_repo)
        print(Fore.GREEN + f'[SUCCESS - GITLAB DELETED] {repo_name} in GITLAB has been deleted')
    else:
        print(Fore.RED + f'[ERROR] {repo_name} not found')
