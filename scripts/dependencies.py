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
    
    # Verificar si pip está instalado
    try:
        import pip
    except ImportError:
        print(Fore.MAGENTA + f" [WARNING] pip is not installed. Attempting to install pip...")
        subprocess.check_call([sys.executable, '-m', 'ensurepip', '--default-pip'])

    # Actualizar pip a la última versión
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])

def install_required_packages(packages):
    for package in packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

if __name__ == "__main__":
    # 1. Comprobar e instalar Python y pip
    check_and_install_python_and_pip()

    # 2. Instalar los paquetes necesarios
    required_packages = ['python-gitlab', 'gitpython', 'PyGithub']
    install_required_packages(required_packages)

