from colorama import init, Fore

init(autoreset=True)

def load_gitlab_vars():
    gl_url = "https://gitlab.com"
    gl_username = input(Fore.CYAN +'Enter your GITLAB username: ')
    gl_token = input(Fore.CYAN +'Enter your GITLAB token: ')
    return gl_url, gl_username, gl_token

def load_github_vars():
    gh_url = "https://api.github.com/user/repos"
    gh_url_general = "https://github.com/"
    gh_url_remove = "https://api.github.com/repos/"
    gh_username = input(Fore.CYAN +'Enter your GITHUB username: ')
    gh_token = input(Fore.CYAN +'Enter your GITHUB token: ')
    return gh_url, gh_url_general, gh_url_remove, gh_username, gh_token

def prompt_repo_name():
    return input(Fore.CYAN +'Enter the repo name: ')
