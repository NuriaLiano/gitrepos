from colorama import Fore, Style, init
import os, json, subprocess
import gitlab
import requests
import utils
init(autoreset=True, convert=True)

def create_gitlab_repo(gl_url, gl_token, repo_name, visibility, org):
    instance = utils.open_gitlab_instance(gl_url, gl_token)
    #check if repo exists
    if utils.check_exists_gitlab_repo(instance, repo_name):
        print(Fore.YELLOW + f'[WARNING] {repo_name} already exists')
        return None
    
    #verify if org had set on parameters
    if org:
        try:
            group = instance.groups.get(org)  # check if org exists
            gl_repo = instance.projects.create({
                'name': repo_name,
                'visibility': visibility,
                'namespace_id': group.id  # Specify the group ID to create the project within the group
            })
        except gitlab.exceptions.GitlabGetError:
            print(Fore.RED + f'[ERROR] Group {org} does not exist.')
            return None
    else:
        # create repo under your user account
        gl_repo = instance.projects.create({'name': repo_name, 'visibility': visibility})

    print(Fore.GREEN + f'[SUCCESS - GITLAB CREATED] {repo_name} created successfully')
    print(Fore.CYAN + f'[CHECK] Go to {gl_repo.http_url_to_repo} to check it!')
    return gl_repo

def clone_new_repo_to_local(gl_repo, main_path, repo_path):
    #change current dir to main path
    os.chdir(main_path)

    #check if repo path exists
    if not os.path.exists(repo_path):
        #clone repo to local
        subprocess.run(["git", "clone", gl_repo.http_url_to_repo])
        print(Fore.GREEN + f'[SUCCESS - GITLAB CLONED] {gl_repo.http_url_to_repo} cloned successfully')
    else:
        print(Fore.YELLOW + f'[WARNING] {repo_path} already exists')

def create_github_repo(gh_url_general, gh_username, gh_token, repo_name, visibility, org_name=None):
    # Determinar la URL de la API en función de si es un usuario o una organización
    if org_name:
        gh_api_repo_url = f"https://api.github.com/orgs/{org_name}/repos"
        gh_repo_url = f"{gh_url_general}{org_name}/{repo_name}"
    else:
        gh_api_repo_url = "https://api.github.com/user/repos"
        gh_repo_url = f"{gh_url_general}{gh_username}/{repo_name}"

    # Crear headers y datos para la solicitud POST
    headers = {
        "Authorization": f"Bearer {gh_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "private": False if visibility == "public" else True
    }

    # Enviar la solicitud POST
    response = requests.post(gh_api_repo_url, headers=headers, json=data)

    # Manejo de la respuesta
    if response.status_code == 201:
        print(Fore.GREEN + f'[SUCCESS - GITHUB CREATED] {repo_name} created successfully')
        print(Fore.CYAN + f'[CHECK] Go to {gh_repo_url} to check it!')
        return response.json()
    elif response.status_code == 404:
        print(Fore.RED + f'[ERROR] Organization or user not found: {org_name if org_name else gh_username}')
        print(Fore.RED + f'[ERROR] Response: {response.json()}')
    elif response.status_code == 403:
        print(Fore.RED + f'[ERROR] Permission denied. Check if the token has the correct scopes.')
        print(Fore.RED + f'[ERROR] Response: {response.json()}')
    else:
        print(Fore.RED + f'[ERROR] {gh_repo_url} failed to create GitHub repository')
        print(Fore.RED + f'[ERROR] Response: {response.json()}')
    return None

def init_local_repo(repo_path, repo_name, github_url):
    #set remote url
    utils.setRemote(repo_path, github_url)
    #create .gitignore
    utils.createGitIgnore(repo_path)
    #create README
    utils.createReadme(repo_path, repo_name)
    #commit changes
    utils.gitCommit(repo_path)
    #push to mirror repos
    utils.gitPushMirror(repo_path)
