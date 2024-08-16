import sys
import subprocess

#initialize colorama
from colorama import init, Fore, Back, Style
init(autoreset=True)
#####################

def check_and_install_python_and_pip():
    # Verificar la versión de Python
    if sys.version_info < (3, 6):
        print(Fore.RED + f'[ERROR] Python 3.6 or higher is required.')
        sys.exit(1)
    
    # check if Pip is installed
    try:
        import pip
    except ImportError:
        print(Fore.MAGENTA + f" [WARNING] pip is not installed. Attempting to install pip...")
        subprocess.check_call([sys.executable, '-m', 'ensurepip', '--default-pip'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # upgrade pip
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def install_required_packages(packages):
    installed = True
    for package in packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            installed = False
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return installed