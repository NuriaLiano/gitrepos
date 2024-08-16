from colorama import Fore, Style, init
import os, json, subprocess
init(autoreset=True, convert=True)

def check_ssh_key():
    home = os.path.expanduser("~")
    ssh_key_path = home + "/.ssh/id_rsa"
    if not os.path.exists(ssh_key_path):
        print(f"{Fore.RED}[ERROR] SSH key file not found.")
    
    print(f"{Fore.GREEN}[SUCCESS] SSH key file founded")

def clone_gitlab_repos(initial_repos_file, main_path):
    #open file and load data
    with open(initial_repos_file, "r") as initial_repos_file:
        json_data = json.load(initial_repos_file)

    for repo_name, repo_info in json_data.items():
        gitlab_url = repo_info.get("gitlab")
        if gitlab_url:
            repo_path = os.path.join(main_path, repo_name)
            if os.path.isdir(repo_path) and os.listdir(repo_path):
                print(f"{Fore.BLUE}[INFO] {repo_name} repo already cloned. Skipping...")
            else:
                print(f"{Fore.BLUE}[INFO] Cloning {gitlab_url} repo into {repo_path}...")
                os.chdir(main_path)
                subprocess.run(["git", "clone", gitlab_url])
        else:
            print(f"{Fore.RED}[ERROR] Gitlab URL not found in {repo_name}. Skipping...")

# def configure_remote_repos(repo_path, github_url):
#     try:
#         # check if remote github is already configured
#         result = subprocess.run(
#             ["git", "-C", repo_path, "remote", "get-url", "github"],
#             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
#         )

#         if result.returncode == 0:
#             print(Fore.BLUE + f"[INFO] Remote 'github' already configured for {repo_path}. Skipping...")
#         else:
#             # Añadir remote github
#             subprocess.run(["git", "-C", repo_path, "remote", "add", "github", github_url], check=True)
#             print(Fore.GREEN + f"[SUCCESS] Configured remote github for {repo_path}")
#     except subprocess.CalledProcessError as e:
#         print(f"{Fore.RED} [ERROR] Error while configuring remotes: {e}")