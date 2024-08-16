from colorama import init, Fore, Back
import os
import check_general_config_file
import utils
import check_requirements
import clone_initial_repos
import local_config_file
import create_repos
import remove_repos
import clone_repo

init(autoreset=True, convert=True)


if __name__ == "__main__":
    print(Fore.LIGHTGREEN_EX + 
    """            
                  __                                              
           __    /\ \__                                           
   __     /\_\   \ \ ,_\   _ __     __    _____     ___     ____  
 /'_ `\   \/\ \   \ \ \/  /\`'__\ /'__`\ /\ '__`\  / __`\  /',__\ 
/\ \L\ \   \ \ \   \ \ \_ \ \ \/ /\  __/ \ \ \L\ \/\ \L\ \/\__, `\\
\ \____ \   \ \_\   \ \__\ \ \_\ \ \____\ \ \ ,__/\ \____/\/\____/
 \/___L\ \   \/_/    \/__/  \/_/  \/____/  \ \ \/  \/___/  \/___/ 
   /\____/                                  \ \_\                 
   \_/__/                                    \/_/                 

___  _   _    ____ _  _ _ _    _    _   _ 
|__]  \_/     [__  |_/  | |    |     \_/  
|__]   |      ___] | \_ | |___ |___   |  

    """)
    print(Fore.LIGHTMAGENTA_EX + "[CHECKING] Checking and configuring GITREPOS :)")
    
    ## check requirements
    print(Fore.LIGHTBLACK_EX + "Checking and installing requirements...")
    check_requirements.check_and_install_python_and_pip()
    ## install required packages
    required_packages = ['python-gitlab', 'gitpython', 'PyGithub']
    if check_requirements.install_required_packages(required_packages):
        print(Fore.GREEN + "[SUCCESS] Requirements installed successfully.")
    else:
        print(Fore.YELLOW + "[WARNING] Some dependencies were installed or updated.")

    ## check main folder
    print(Fore.LIGHTBLACK_EX + "Checking main folder...")
    ## don't enter the / in the params
    check_general_config_file.check_or_create_main_folder("gitlab")

    ## check general config file
    print(Fore.LIGHTBLACK_EX + "Checking general config file...")
    check_general_config_file.check_or_create_general_config_file()

    ## load config data
    main_vars = utils.load_main_vars()
    ## check if ssh key is present in .ssh folder
    print(Fore.LIGHTBLACK_EX + "Checking SSH key...")
    clone_initial_repos.check_ssh_key()

    option = input(Fore.CYAN + "Do you want to clone initial repos? y/n: ").lower()

    if option == "y":
        ## clone gitlab repos
        print(Fore.LIGHTBLACK_EX + "Cloning gitlab repos...")
        clone_initial_repos.clone_gitlab_repos("data/initial_repos.json", main_vars["config"]["MAIN_PATH"])

        ## configure remote repos
        print(Fore.LIGHTBLACK_EX + "Configuring remote repos...")
        for repo_name, repo_info in main_vars["repos"].items():
            ## generate vars repo path and github url
            repo_path = main_vars["config"]["MAIN_PATH"] + "\\" +repo_name
            github_url = repo_info.get("github")
            utils.setRemote(repo_path, github_url)

    print(Back.CYAN + "Hello! This is gitrepos tool for gitlab and github. Enjoy it! :)")

    ## prompt if create/remove/clone repos
    action = input(Fore.CYAN + "Do you want create, remove or clone repo? c/r/d: ").lower()

    if action == "c":
        print(Fore.LIGHTBLACK_EX + "Creating repo...")
        user_org = input(Fore.CYAN + "User or Skilly? u/s: ")
        repo_name = input(Fore.CYAN + "Enter repo name: ")
        visibility = utils.set_visibility()
        

        #create gitlab
        print(Fore.LIGHTBLACK_EX + "Creating gitlab repo...") 
        gl_url = main_vars["config"]["GL_URL"]
        gl_token = main_vars["config"]["GL_TOKEN"]
        organization = main_vars["config"]["ORGANIZATION"] if user_org == "s" else None
        gl_repo = create_repos.create_gitlab_repo(gl_url, gl_token, repo_name, visibility, organization)
        if not gl_repo:
            print(Fore.RED + "[ERROR] GitLab repo creation failed. Aborting operation.")
            exit(1)

        #clone to local
        repo_path = main_vars["config"]["MAIN_PATH"] + "\\" + repo_name
        print(Fore.LIGHTBLACK_EX + "Cloning gitlab repo to local...")
        create_repos.clone_new_repo_to_local(gl_repo, main_vars["config"]["MAIN_PATH"], repo_path)

        #create github
        print(Fore.LIGHTBLACK_EX + "Creating github repo...")
        gh_api_url = main_vars["config"]["GH_API_URL"]
        gh_url = main_vars["config"]["GH_URL"]
        gh_url_general = main_vars["config"]["GH_URL_GENERAL"]
        gh_username = main_vars["config"]["GH_USERNAME"]
        gh_token = main_vars["config"]["GH_TOKEN"]
        create_repos.create_github_repo(gh_url_general, gh_username, gh_token, repo_name, visibility, organization)
        
        #init local repo
        print(Fore.LIGHTBLACK_EX + "Initializing local repo...")
        gh_username_or_org = main_vars["config"]["ORGANIZATION"] if user_org == "s" else main_vars["config"]["GH_USERNAME"]
        github_url = f'{main_vars["config"]["GH_URL_GENERAL"]}{gh_username_or_org}/{repo_name}.git'
        create_repos.init_local_repo(repo_path, repo_name, github_url)

    elif action == "r":
        print(Fore.LIGHTBLACK_EX + "Removing repo...")
        remove_prompt = input(Fore.YELLOW + '[WARNING] Are you sure you want to delete the repository? y/n: ').lower()
        user_org = input(Fore.CYAN + "User or Skilly? u/s: ").lower()
        remove_repo_name = input(Fore.CYAN + "Enter repo name to remove: ")
        if remove_prompt == "y":
            gh_api_url = main_vars["config"]["GH_API_URL"]
            gh_username = main_vars["config"]["GH_USERNAME"]
            gh_token = main_vars["config"]["GH_TOKEN"]
            org_name = main_vars["config"]["ORGANIZATION"] if user_org == "s" else None
            remove_repos.remove_github(remove_repo_name, gh_api_url, gh_token, gh_username, org_name)

            gl_url = main_vars["config"]["GL_URL"]
            gl_token = main_vars["config"]["GL_TOKEN"]
            remove_repos.remove_gitlab(remove_repo_name, gl_url, gl_token)

            remove_repos.remove_local(main_vars["config"]["MAIN_PATH"], remove_repo_name)
        else:
            print(Fore.RED + '[INFO] Operation cancelled.')
    elif action == "d":
        print(Fore.LIGHTBLACK_EX + "Cloning repo...")
        repo_name = input(Fore.CYAN + "Enter repo name to clone: ")
        main_path =  main_vars["config"]["MAIN_PATH"]
        gl_url =  main_vars["config"]["GL_URL"]
        gl_token =  main_vars["config"]["GL_TOKEN"]
        gh_url_general =  main_vars["config"]["GH_URL_GENERAL"]
        gh_username =  main_vars["config"]["GH_USERNAME"]
        gh_org = main_vars["config"]["ORGANIZATION"]
        clone_repo.clone_repos(repo_name, main_path, gl_url, gl_token, gh_url_general, gh_username, gh_org)
                                
