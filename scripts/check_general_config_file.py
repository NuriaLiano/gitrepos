import os
import json
import local_config_file, utils
from colorama import Fore, Style, init

init(autoreset=True, convert=True)

def check_or_create_main_folder(main_folder):
    home = os.path.expanduser("~")
    main_path = home + "/" + main_folder

    if not os.path.exists(main_path):
        print(f"{Fore.YELLOW}[WARNING] Creating main folder: {main_path}")
        #change current dir to home path
        os.chdir(home)
        #create main folder
        os.makedirs(main_path)
    
    print(f"{Fore.GREEN}[SUCCESS] Main folder already exists: {main_path}")



def check_or_create_general_config_file():
    main_path = os.path.join(os.path.expanduser("~"), "gitlab")
    config_filename = ".config.json"
    config_path = os.path.join(main_path, config_filename)

    if os.path.exists(config_path):
        print(Fore.BLUE + f"[INFO] Config file already exists: {config_path}")
        with open(config_path, "r") as config_file:
            config_data = json.load(config_file)
        return config_data
    else:
        local_config_file.create_config_file(config_path)
        #prompt vars 
        gl_url, gl_username, gl_token, gl_org = utils.prompt_gitlab_vars()
        gh_url, gh_url_general, gh_api_url, gh_username, gh_token, gh_org = utils.prompt_github_vars()
        local_config_file.add_data_to_config('EMAIL', utils.get_gitConfig("user.email"), config_path)
        local_config_file.add_data_to_config('GL_USERNAME', gl_username, config_path)
        local_config_file.add_data_to_config('GL_TOKEN', gl_token, config_path)
        local_config_file.add_data_to_config('GL_URL', gl_url, config_path)
        local_config_file.add_data_to_config('GL_ORG', gl_org, config_path)
        local_config_file.add_data_to_config('GH_USERNAME', gh_username, config_path)
        local_config_file.add_data_to_config('GH_TOKEN', gh_token, config_path)
        local_config_file.add_data_to_config('GH_URL', gh_url, config_path)
        local_config_file.add_data_to_config('GH_URL_GENERAL', gh_url_general, config_path)
        local_config_file.add_data_to_config('GH_API_URL', gh_api_url, config_path)
        local_config_file.add_data_to_config('GH_ORG', gh_org, config_path)
        local_config_file.add_data_to_config('MAIN_FOLDER', "gitlab", config_path)
        local_config_file.add_data_to_config('MAIN_PATH', main_path, config_path)
        print(Fore.GREEN + f'[SUCCESS] {config_path} saved successfully')
