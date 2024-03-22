import requests
from colorama import Fore
import os
import json

blue = Fore.CYAN
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
pinkigualppk = Fore.MAGENTA
reset = Fore.RESET

validos = 0
invalidos = 0
nitros = 0
verificadas = 0
mfa = 0
billing = 0

def verificar_tokens_arquivo(arquivo_entrada, arquivo_funcionando, arquivo_nao_funcionando):
    with open(arquivo_entrada, 'r') as arquivo_tokens:
        tokens = arquivo_tokens.read().splitlines()
    
    for token in tokens:
        if verificar_token(token):
            with open(arquivo_funcionando, 'a') as arquivo_func:
                arquivo_func.write(token + '\n')
        else:
            with open(arquivo_nao_funcionando, 'a') as arquivo_nao_func:
                arquivo_nao_func.write(token + '\n')
    print(f"{blue}[FINALIZADO]{reset} {pinkigualppk}|{reset} {green}VÁLIDOS{reset}: {validos} - {red}INVÁLIDOS{reset}: {invalidos} - {pinkigualppk}NITRO{reset}: {nitros} - {blue}VERIFICADAS{reset}: {verificadas} - {red}MFA{reset}: {mfa} - {green}BILLING{reset}: {billing}")

def verificar_token(token):
    global validos, invalidos, nitros, verificadas, billing, mfa
    url = "https://discord.com/api/v9/users/@me"
    headers = {
        "Authorization": token
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        validos += 1
        dados = response.json()
        premium_type = dados.get('premium_type', 0)
        username = dados.get('username', False)
        mfa_enabled = dados.get('mfa_enabled', False)
        verified = dados.get('verified', False)
        
        premium_tipo = "Nenhum"
        if premium_type == 1:
            premium_tipo = "Nitro Basic"
            nitros += 1
        elif premium_type == 2:
            premium_tipo = "Nitro Gaming"
            nitros += 1
        
        mfa = "Habilitado" if mfa_enabled else "Desabilitado"
        verificado = "Sim" if verified else "Não"
        if verificado == "Sim":
            verificadas += 1
        else:
            verificadas += 0
        if mfa == "Habilitado":
            mfa += "1"
        else:
            pass

        url = "https://ptb.discord.com/api/v9/users/@me/billing/payment-sources"
        headers = {
            "authorization": token
        }
        response = requests.get(url, headers=headers)
        json_data = response.json()
        numero_de_cartoes = json_data.count('"id"')
        billing += numero_de_cartoes
        print(f"{green}[VÁLIDO]{reset} {pinkigualppk}|{reset} {token[:10]}**** {pinkigualppk}|{reset} {blue}MFA:{reset} {mfa} {pinkigualppk}|{reset} {blue}Verificada:{reset} {verificado} {pinkigualppk}|{reset} {blue}Nitro:{reset} {premium_tipo} {pinkigualppk}|{reset} {blue}Nome:{reset} {username} {pinkigualppk}|{reset} {blue}Billing:{reset} {numero_de_cartoes}")
    else:
        print(f"{red}[INVÁLIDO]{reset} {pinkigualppk}|{reset} {token[:55]}****")
        invalidos += 1
    return response.status_code == 200

# Arquivos de entrada e saída
arquivo_entrada = "input/tokens.txt"
arquivo_funcionando = "input/tokens_funcionando.txt"
arquivo_nao_funcionando = "input/tokens_nao_funcionando.txt"

# Chamada da função para verificar os tokens do arquivo
os.system('cls')
print(f"""
 ▄████  █     ██  ██▓ ██▓     ██░ {blue}██ ▓█████  ██▀███   ███▄ ▄███▓▓█████{reset}
 ██▒ ▀█▒ ██  ▓██▒▓██▒▓██▒    ▓██░ {blue}██▒▓█   ▀ ▓██ ▒ ██▒▓██▒▀█▀ ██▒▓█   ▀ {reset}
▒██░▄▄▄░▓██  ▒██░▒██▒▒██░    ▒██▀▀{blue}██░▒███   ▓██ ░▄█ ▒▓██    ▓██░▒███{reset}
░▓█  ██▓▓▓█  ░██░░██░▒██░    ░▓█ ░{blue}██ ▒▓█  ▄ ▒██▀▀█▄  ▒██    ▒██ ▒▓█  ▄ {reset}
░▒▓███▀▒▒▒█████▓ ░██░░██████▒░▓█▒░{blue}██▓░▒████▒░██▓ ▒██▒▒██▒   ░██▒░▒████▒{reset}
 ░▒   ▒ ░▒▓▒ ▒ ▒ ░▓  ░ ▒░▓  ░ ▒ ░░{blue}▒░▒░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░   ░  ░░░ ▒░ ░{reset}
  ░   ░ ░░▒░ ░ ░  ▒ ░░ ░ ▒  ░ ▒ ░▒{blue}░ ░ ░ ░  ░  ░▒ ░ ▒░░  ░      ░ ░ ░  ░{reset}
░ ░   ░  ░░░ ░ ░  ▒ ░  ░ ░    ░  ░{blue}░ ░   ░     ░░   ░ ░      ░      ░{reset}
      ░    ░      ░      ░  ░ ░  ░{blue}  ░   ░  ░   ░            ░      ░  ░{reset}
""")
input("pressione enter para começar a verificar: ")
verificar_tokens_arquivo(arquivo_entrada, arquivo_funcionando, arquivo_nao_funcionando)
