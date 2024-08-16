import subprocess
import gitlab
import git
from colorama import Fore, init
import os
import utils
init(autoreset=True, convert=True)

def find_and_clone_repo(repo_name, main_path, gl_url, gl_token, gh_url_general, gh_username, gh_org):
    instance = gitlab.Gitlab(gl_url, private_token=gl_token)

    # search in user account 
    try:
        user_repo = instance.projects.get(f'{gh_username}/{repo_name}')
        repo_url = user_repo.ssh_url_to_repo
        print(Fore.GREEN + f'[SUCCESS] Found repository "{repo_name}" in user account "{gh_username}".')
    except gitlab.exceptions.GitlabGetError:
        user_repo = None
        print(Fore.YELLOW + f'[INFO] Repository "{repo_name}" not found in user account.')

    # if not found, search in organization
    if not user_repo:
        try:
            org_repo = instance.projects.get(f'{gh_org}/{repo_name}')
            repo_url = org_repo.ssh_url_to_repo
            print(Fore.GREEN + f'[SUCCESS] Found repository "{repo_name}" in organization "{gh_org}".')
        except gitlab.exceptions.GitlabGetError:
            org_repo = None
            print(Fore.RED + f'[ERROR] Repository "{repo_name}" not found in both user and organization.')

    # clone repo
    if user_repo or org_repo:
        print(Fore.LIGHTBLACK_EX + f'[INFO] Cloning repository to {main_path + repo_name}...')
        os.chdir(main_path)
        subprocess.run(["git", "clone", repo_url])
        print(Fore.GREEN + f'[SUCCESS] Cloned repository "{repo_name}" successfully.')        

        # configure remotes
        github_url = f'{gh_url_general}{gh_org if org_repo else gh_username}/{repo_name}.git'
        utils.setRemote(main_path + repo_name, github_url)