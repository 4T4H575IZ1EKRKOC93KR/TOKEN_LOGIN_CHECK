import sys, subprocess
print("[✔] Vérification...")
for p in ["requests","emoji","tabulate","selenium","webdriver-manager","colorama","rich","discord.py","psutil","mss","pyautogui","aiohttp","aiofiles","pyperclip"]:
    try: __import__(p.replace("-","_"))
    except: print("[+] Installation...");subprocess.check_call([sys.executable,"-m","pip","install",p],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print("[✅] OK.")
import time,threading,emoji,re,random, string, requests, getpass
import requests as r,subprocess as s,os as o,webbrowser as w
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from colorama import init, Fore, Style
from rich.console import Console
from rich.text import Text
init(autoreset=True)
def get_user_info(token, is_bot=False):
    headers = {
        "Authorization": f"{'Bot ' if is_bot else ''}{token}"
    }
    response = r.get("https://discord.com/api/v10/users/@me", headers=headers)
    return response
def replace_emojis_with_text(text):
    return emoji.demojize(text)
def print_result(result, token_type):
    filtered_result = {key: value for key, value in result.items() if key not in ['clan', 'primary_guild']}
    for key, value in filtered_result.items():
        if isinstance(value, str):
            filtered_result[key] = replace_emojis_with_text(value)
    table_headers = [f"{Fore.BLUE}Clé", f"{Fore.BLUE}Valeur"]
    table_data = [
        [f"{Fore.WHITE}Type de Token", f"{Fore.GREEN}{token_type}"],
        [f"{Fore.WHITE}ID Utilisateur", f"{Fore.YELLOW}{filtered_result.get('id', 'N/A')}"],
        [f"{Fore.WHITE}Nom d'utilisateur", f"{Fore.YELLOW}{filtered_result.get('username', 'N/A')}#{filtered_result.get('discriminator', 'N/A')}"],
        [f"{Fore.WHITE}Email", f"{Fore.YELLOW}{filtered_result.get('email', '[Non disponible]')}"],
        [f"{Fore.WHITE}Téléphone", f"{Fore.YELLOW}{filtered_result.get('phone', '[Non disponible]')}"],
    ]
    for key, value in filtered_result.items():
        if key not in ['email', 'phone']:
            table_data.append([f"{Fore.WHITE}{key.capitalize()}", f"{Fore.CYAN}{value}"])
    clear_console()
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Résultats de la vérification du Token ===\n")
    print(tabulate(table_data, headers=table_headers, tablefmt="fancy_grid"))
    print(f"\n{Fore.GREEN}{Style.BRIGHT}=========================\n")
def print_centered(text, color=""):
    console_width = o.get_terminal_size().columns
    centered_text = text.center(console_width)
    print(f"{color}{centered_text}{Style.RESET_ALL}")
def print_large_text(text, color="cyan"):
    console = Console()
    console_height = o.get_terminal_size().lines
    console_width = o.get_terminal_size().columns
    text = Text(text, style=color)
    vertical_padding = (console_height - 3) // 2
    console.print("\n" * vertical_padding)
    console.print(text, justify="center", width=console_width)
    console.print("\n" * vertical_padding)
def loader():
    for c in "|/-\\":
        sys.stdout.write(f"\r{Fore.YELLOW}Connexion en cours... {c}")
        sys.stdout.flush()
        time.sleep(0.1)
def clear_console():
    o.system('cls' if o.name == 'nt' else 'clear')
def display_error(message):
    print(f"{Fore.RED}{Style.BRIGHT}❌ {message}")
    sys.exit(1)
def connect_to_discord(token):
    print(f"{Fore.BLUE}Lancement du navigateur Chrome...")
    options = Options()
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        clear_console()
        print(f"{Fore.BLUE}❌ Erreur lors de l'initialisation du navigateur télécharge Chrome : https://www.google.com/chrome/")
        print(f"""
    {Fore.RED}⚠️ Google Chrome est requis pour exécuter ce programme correctement.
        {Fore.GREEN}{Style.BRIGHT}Le navigateur est utilisé en arrière-plan pour automatiser certaines tâches.
        Vous pouvez le désinstaller après utilisation si vous le souhaitez, 
        mais sans Chrome, l'application ne pourra pas fonctionner.
        """)
        w.open("https://www.google.com/chrome/")
        return
    driver.get("https://discord.com/login")
    time.sleep(2)
    print(f"{Fore.BLUE}Injection du token et connexion en cours...")
    t = threading.Thread(target=loader)
    t.start()
    js_code = f"""
    function login(token) {{
      setInterval(() => {{
        document.body.appendChild(document.createElement(`iframe`)).contentWindow.localStorage.token = `"${{token}}"`;
      }}, 50);
      setTimeout(() => {{
        location.reload();
      }}, 2500);
    }}
    login("{token}")
    """
    try:
        driver.execute_script(js_code)
    except Exception as e:
        display_error(f"Erreur lors de l'injection du token : {str(e)}")
    t.join()
    print(f"\n{Fore.GREEN}{Style.BRIGHT}✅ Connexion réussie ! Le navigateur est ouvert.\n")
    print(f"{Fore.YELLOW}Vous pouvez maintenant utiliser Discord comme si vous étiez connecté normalement.")
    input("")
def main():
    clear_console()
    print_large_text("=== Discord Token Checker ===", "cyan")
    while True:
        token = input(f"{Fore.YELLOW}Entrez le token à vérifier : ").strip()
        token = token.replace(" ", "")
        if not token:
            print(f"{Fore.RED}❌ {Fore.WHITE}Vous devez entrer un token valide.\n")
            continue
        result = None
        token_type = None
        error = None
        response = get_user_info(token, is_bot=False)
        if response.status_code == 200:
            token_type = "Utilisateur"
            result = response.json()
        else:
            response = get_user_info(token, is_bot=True)
            if response.status_code == 200:
                token_type = "Bot"
                result = response.json()
            else:
                error = f"Token invalide."
                try:
                    result = response.json()
                except:
                    result = {"message": "Aucune réponse JSON"}
        if error:
            clear_console()
            print(f"{Fore.CYAN}{Style.BRIGHT}=== Discord Token Checker ===\n")
            print(f"{Fore.RED}❌ Veuillez entrer un token valide.")
            continue
        if result:
            print_result(result, token_type)
            connect_choice = input(f"{Fore.GREEN}Souhaitez-vous vous connecter à Discord avec ce token ? (Y/N) ").strip().lower()
            if connect_choice == 'y':
                connect_to_discord(token)
                break
            elif connect_choice == 'n':
                print(f"{Fore.RED}Déconnexion... Le programme va maintenant quitter.")
                time.sleep(2)
                clear_console()
                break
            else:
                print(f"{Fore.RED}❌ Choix invalide. Veuillez entrer 'Y' ou 'N'.\n")
if __name__ == "__main__":
    main()