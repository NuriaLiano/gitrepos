import subprocess
from colorama import init, Fore

init(autoreset=True)

def run_script(script_name):
    try:
        result = subprocess.run(['python', script_name], check=True)
        if result.returncode != 0:
            print(Fore.RED + f'[ERROR] {script_name} failed to execute.')
            exit(result.returncode)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f'[ERROR] {script_name} failed to execute with error: {e}')
        exit(e.returncode)
    except Exception as e:
        print(Fore.RED + f'[ERROR] Failed to run {script_name}: {e}')
        exit(1)

def main():
    print(Fore.CYAN + 'Running dependencies.py...')
    run_script('./scripts/dependencies.py')

    print(Fore.CYAN + 'Running clone_repos.py...')
    run_script('./scripts/clone_repos.py')

    print(Fore.CYAN + 'Running repo_management.py...')
    run_script('./scripts/repo_management.py')

    print(Fore.GREEN + '[SUCCESS] All scripts executed successfully!')

if __name__ == '__main__':
    main()
