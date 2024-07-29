<div align="center">
  <img src="./img/gitrepos_bck.png" alt="tabla de los tipos de datos" style="width:100vw; height:40vh;">
</div>

## What is GITREPOS

GITREPOS is a Python script designed to automate the management of repository creation, deletion, and mirroring between GitHub and GitLab. It facilitates seamless synchronization across these platforms, simplifying version control operations for developers.

## Contents of GITREPOS repository

- **gitrepos.py**: The main Python script for running all other scripts in order, ensuring dependencies are met and repositories are managed.
- **scripts/dependencies.py**: Checks and installs required dependencies.
- **scripts/clone_repos.py**: Clones repositories based on a configuration file.
- **scripts/repo_management.py**: Manages the creation, configuration, and deletion of repositories.
- **scripts/config.py**: Handles configuration file operations.
- **scripts/git_utils.py**: Utility functions for Git operations.
- **scripts/github_utils.py**: Utility functions for GitHub operations.
- **scripts/gitlab_utils.py**: Utility functions for GitLab operations.
- **scripts/prompts.py**: Handles user input prompts.
- **scripts/utils.py**: General utility functions.
- **gitPushMirror.sh**: A Bash script to synchronize commits across mirrored repositories using `git push`.
- **requirements.txt**: Lists all dependencies required to run the scripts.
- **container.config.json**: Sample configuration file for global settings related to your repositories.
- **local.config.json**: Sample configuration file for individual repository settings.

## Prerequisites
The first time you run the script it will ask for all the variables it does not find and generate the `.config.json` file both in the container and locally.

- Python 3.6 or newer.
- Git 2.39 or newer.
- Ensure that Git Bash is installed if running on Windows for script execution.

### Gitlab data

- **Username**: "Nuria_Liano"
- **Gitlab Token**: "asa7f9sd87fsg8sd987sd8g8s"

### Github data

- **Username**: "NuriaLiano"
- **Github Token**: "asa7f9sd87fsg8sd987sd8g8s"

## How to run

:warning: **You must have Python 3.6 or newer and GIT 2.39 or newer installed on your local system** :warning:

### 1. First of all, you must create a container directory where all repositories will be stored

Example: my container configuration

- gitlab (container)
  - gitrepos (repo1)
  - personalRepo (repo2)
  - otherRepos (repo3)

### 2. Download or clone this repository

- Download the script: `wget https://gitlab.com/Nuria_Liano/gitrepos/-/raw/main/gitrepos.py?inline=false`
- Clone the repository
  - SSH:  `git clone git@gitlab.com:Nuria_Liano/gitrepos.git`
  - HTTPS:  `git clone https://gitlab.com/Nuria_Liano/gitrepos.git`

### 3. Install all requirements

- Python: `pip install -r requirements.txt`

### 4. Configure the Remote Repositories

>:pencil: Check your current remote repository configuration with the following command
> ``git remote -v``

```sh
git remote add github https://github.com/yourUser/yourRepo.git
```
### 5. :exclamation: Important steps :exclamation: Edit the container.config.json file and change the file name to '.config.json'

This file contains all necessary global variables to execute the script. You must change all values for your own data.

~~~json
{
    "EMAIL": "nuria@email.com",
    "GH_USERNAME": "nuria",
    "GL_USERNAME": "nuria",
    "GH_TOKEN": "ghsdfsdgssdhPewghrBOnhgfdhdfX",
    "GL_TOKEN": "ghsdfsdgssdhPewghrBOnhgfdhdfX",
    "GH_URL": "https://api.github.com/nuria/repos",
    "GH_URL_GENERAL": "https://github.com/",
    "GL_URL": "https://gitlab.com",
    "GH_URL_REMOVE": "https://api.github.com/repos/"
}
~~~

> :pencil: When you finish editing, it is important to rename the file to '.config.json' and move it to your container git directory.

### :exclamation: Important steps :exclamation: Edit the local.config.json file and change the file name to '.config.json'

This file contains all necessary local repo variables to execute the script. You must change all values for your own data.

~~~json
{
    "LOCAL_PATH": "C:\\Users\\nuria\\gitlab\\gitrepos",
    "LOCAL_PATH_CONFIG": "C:\\Users\\nuria\\gitlab\\gitrepos\\.config.json",
    "GL_VISIBILITY": "public",
    "GL_ID_REPO": 8937492,
    "GL_REPO_URL": "https://gitlab.com/Nuria_Liano/gitrepos.git",
    "GH_VISIBILITY": "public",
    "GH_PROJECT_URL": "https://api.github.com/repos/Nuria_Liano/gitrepos",
    "GH_REPO_URL": "https://github.com/Nuria_Liano/gitrepos",
    "DEFAULT_BRANCH": "master",
    "README_PATH": "C:\\Users\\nuria\\gitlab\\gitrepos\\README.md"
}
~~~

> :pencil: When you finish editing, it is important to rename the file to '.config.json'. Keep it in the repo.

### 7. Execute script

~~~sh
python gitrepos.py
~~~

### 8. Now you can use that repository and you can execute git add and git commit -m "" normally

### 9. :warning: But when you execute git push it is necessary to run the gitPushMirror.sh

~~~sh
sh gitPushMirror.sh
~~~

## Example of execution

1. Run gitrepos.py

~~~sh
'COMMAND'
$ python {your_path}/gitrepos.py

'OUTPUT'
Do you want to remove or create a new repo? r/c: c
Enter the repo name: testRepo
[SUCCESS - CHECK CONTAINER CONFIG] gitlab\.config.json loaded successfully
[SUCCESS - LOCAL CREATED] \gitlab\testRepo created successfully
Enter the repo visibility: (public/private)
[WARNING] press enter to set the repo visibility to "public"
[SUCCESS - GITLAB CREATED] testRepo created successfully
[CHECK] Go to https://gitlab.com/Nuria_Liano/testRepo.git to check it!
Enter the repo visibility: (public/private)
[WARNING] press enter to set the repo visibility to "public"
[SUCCESS - GITHUB CREATED] testRepo created successfully
[CHECK] Go to https://api.github.com/repos/NuriaLiano/testRepo to check it!
[SUCCESS - README CREATED] \gitlab\testRepo/README.md created successfully
[SUCCESS - README COMMITED] \gitlab\testRepo/README.md committed successfully
[SUCCESS - README PUSHED] Push with upstream master
[SUCCESS - MIRROR SET UP] https://github.com/NuriaLiano/testRepo set up successfully
~~~

2. Add data and files

~~~sh
touch README.md
~~~

3. Git add and git commit

~~~sh
'COMMAND'
$ git add README.md
$ git commit -m "update Readme"

'OUTPUT'
[master 0933f14] update Readme
 1 file changed, 47 insertions(+)
~~~

4. Git push mirror

~~~sh
'COMMAND'
$ sh gitPushMirror.sh

'OUTPUT' 
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 312 bytes | 312.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
To https://gitlab.com/Nuria_Liano/gitrepos.git
   ba06cf8..c4f36cf  master -> master
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 312 bytes | 312.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/NuriaLiano/gitrepos
   ba06cf8..c4f36cf  master -> master
Everything up-to-date
~~~

5. (Optional) Remove repository

~~~sh
'COMMAND'
$ python {your_path}/gitrepos.py

'OUTPUT'
Do you want to remove or create a new repo? r/c: r
Enter the repo name: testRepo
Are you sure you want to delete the repository? y/n: y
[SUCCESS - GITHUB DELETE] https://api.github.com/repos/NuriaLiano/testRepo deleted successfully
[SUCCESS - GITLAB DELETED] testRepo in GITLAB has been deleted
[SUCCESS - LOCAL DELETED] \gitlab\testRepo has been deleted
~~~

## How to generate a mirror

The set_up_gitlab_github_mirror function is responsible for setting up a mirror between a GitLab repository and a GitHub repository. Here's the step-by-step of how it does this setup:

- **Gets the necessary variables**: the function starts by getting the paths to the directories and files needed for the mirror setup. It uses the create_path function to create the paths to the local directories and the configuration file local_path_config. In addition, it gets the URLs of the GitLab and GitHub repositories, as well as the GitHub access token, from the container_path_config configuration file.
- **Add the GitHub repository as a remote**: Use the gitpython library to add the GitHub repository as a remote named "github" to the local GitLab repository. This is accomplished with the line gitlabRepo.create_remote('github', gh_repo_url). This way, the local GitLab repository is configured to push changes to the GitHub repository via the remote "github".
- **Configure the mirror in GitLab**: Use the Git command line tool to configure the mirror between the GitLab repository and the GitHub repository. This is done through the following lines of code:

~~~py
gitlabRepo.git.remote('set-url', '--push', 'github', gh_repo_url)
gitlabRepo.git.remote('set-url', '--push', '--add', 'github', gl_repo_url)
~~~

These lines set the push URLs for the remote "github" so that changes made to the local GitLab repository are automatically pushed to the GitHub repository. gh_repo_url represents the URL of the GitHub repository and gl_repo_url represents the URL of the GitLab repository.

- **Synchronize changes**: The function gets the name of the active branch in the local GitLab repository by default_branch = gitlabRepo.active_branch.name. It then performs a pull operation from the GitLab repository to get the most recent changes to the active branch, using the line gitlabRepo.remotes.origin.pull(default_branch). It then performs a push operation on the "github" remote to push the changes to the GitHub repository, using the GitHub access token for authentication:

~~~sh
gitlabRepo.git.push('--all', 'github', **{'o': f'oauth2accesstoken:{gh_token}'})
~~~

## Errors and suggestions

If you find a problem with the code or have implemented an improvement, please open an issue.

> :warning: Windows Users
> When running the gitPushMirror.sh script, you might need to set the script as executable using Git Bash

## TODO

- [x] generate .gitignore to ignore .config.json
- [x] add remote 
- [x] check dependencies
- [ ] gitPushBot: script that checks for changes in the repo every X minutes and executes gitPushMirror.sh automatically.ç

## License

All content in this repository is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International Public License](https://gitlab.com/skilly-academy/gitrepos/-/blob/master/LICENSE)

## Contact

You can write to me at hola@nurialiano.es

Visit my profiles or my website

<div>
    <p align="center">
        <a href="https://www.twitch.tv/nurialiano" target="_blank"><img height="50" src="https://github.com/NuriaLiano/NuriaLiano/raw/master/img/icons/twitch.svg" /></a>
        <a href="https://gitlab.com/nuria_liano" target="_blank"><img height="50" src="https://github.com/NuriaLiano/NuriaLiano/raw/master/img/icons/gitlab.svg" /></a>
        <a href="https://github.com/nurialiano" target="_blank"><img height="50" src="https://github.com/NuriaLiano/NuriaLiano/raw/master/img/icons/github.svg" /></a>
        <a href="https://twitter.com/nuria_liano" target="_blank"><img height="50" src="https://github.com/NuriaLiano/NuriaLiano/raw/master/img/icons/twitter.svg"  /></a>
        <a href="https://www.buymeacoffee.com/lianonuria" target="_blank"><img height="50" src="https://github.com/NuriaLiano/NuriaLiano/raw/master/img/icons/by-me-a-coffee.png" /></a>
    </p>
</div>

---

Desarrollado en [cantabria](https://www.cantabria.es)💢 con mucho 🤘 y 🍺