# Bibliotecas utlizadas para requisições de uma HTTP, manipulação de JSON e criaçaõ de arquivos e diretórios 
import requests
import json
import os

# Importa as configurações do arquivo settings.py e a tipagem Dict que define um dicionário
from config.settings import SETTINGS
from typing import Dict

# Define o Json como um dicionário de strings
Json = Dict[str, str]

# Função que busca o total de vagas como número inteiro
def buscando_valor_total(palavra: str) -> int:

    url = f'https://portal.api.gupy.io/api/job?name={palavra}&offset=0&limit=10'
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        return dados.get("pagination").get("total", 0)
    return 0

# Função que busca as vagas de emprego baseando-se na palavra-chave definidade em settings.py
def buscar_vagas(vaga: str) -> Json:
    
    todas_vagas = []
    SETTINGS["file_path"] = os.path.join("data", "vagas_gupy.json")
    os.makedirs(os.path.dirname(SETTINGS["file_path"]), exist_ok=True)

    for palavra in SETTINGS["palavras_chave"]:
        print(f"\nBuscando vagas para: {palavra}")

# Trecho de código que busca as vagas na API da Gupy 
        total = buscando_valor_total(palavra)
        offset = 0 
        for _ in range(0, total, 10):
    
            url = f'https://portal.api.gupy.io/api/job?name={vaga}&offset={offset}&limit=10'
            resposta = requests.get(url) 
            if resposta.status_code != 200:
                break
            
# Trecho de código que armazena as vagas em uma lista
            dados = resposta.json()

            if "data" in dados:
                print(f"Vagas encontradas: {len(dados['data'])}")
                todas_vagas.extend(dados.get("data", []))
            offset += 10

# STrecho de código quesalva as vagas em um arquivo JSON
    with open(SETTINGS["file_path"], "w", encoding="utf-8") as gupy:
        json.dump(todas_vagas, gupy, ensure_ascii=False, indent=2) 
