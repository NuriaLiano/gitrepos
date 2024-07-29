import os
import json
import git
from colorama import init, Fore

init(autoreset=True, convert=True)

def clone_and_add_remotes(repos):
    # Obtener el directorio padre del directorio actual
    parent_dir = os.path.dirname(os.getcwd())
    
    for repo, remotes in repos.items():
        repo_name = repo.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(parent_dir, repo_name)
        
        if not os.path.exists(repo_path):
            print(Fore.CYAN + f"Cloning {repo} into {repo_path}...")
            git.Repo.clone_from(repo, repo_path)
        else:
            print(Fore.YELLOW + f"Repository {repo_name} already exists. Skipping clone.")
        
        repo_obj = git.Repo(repo_path)
        
        for remote_name, remote_url in remotes.items():
            if remote_name not in [r.name for r in repo_obj.remotes]:
                repo_obj.create_remote(remote_name, remote_url)
                print(Fore.GREEN + f"Added remote {remote_name} with URL {remote_url} to {repo_name}")
            else:
                print(Fore.YELLOW + f"Remote {remote_name} already exists in {repo_name}. Skipping.")

def load_repos_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    repos_config = load_repos_config('data/repos.json')
    clone_and_add_remotes(repos_config)
