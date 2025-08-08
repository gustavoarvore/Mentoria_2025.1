#Biblioteca para buscar vagas de emprego na Gupy
import requests
import json
import os

from config.settings import SETTINGS
from typing import Dict

Json = Dict[str, str]

# Faz uma requisição para a API da Gupy com as palavras-chave e offsets definidos
def buscar_vagas(vaga: str) -> Json:
    if not isinstance(vaga, str):
        return print ("A palavra-chave deve ser uma string.")
    
    todas_vagas = []
    SETTINGS["file_path"] = os.path.join("data", "vagas_gupy.json")
    os.makedirs(os.path.dirname(SETTINGS["file_path"]), exist_ok=True)

    for palavra in SETTINGS["palavras_chave"]:
        print(f"\nBuscando vagas para: {palavra}")

# Itera sobre os offset para buscar todas as vagas disponíveis
    for offset in SETTINGS["offset"]:
        url = f'https://portal.api.gupy.io/api/job?name={vaga}&offset={offset}&limit=10'
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            
# Processa a resposta JSON e extrai as vagas
            if "data" in dados:
                print(f"Vagas encontradas: {len(dados['data'])}")
                todas_vagas.extend(dados.get("data", []))

    # Adiciona a paginação ao resultado
    total_vagas = len(todas_vagas)
    resultado = {
        "lista": todas_vagas,
        "pagination": {
            "offset": 0,                      # O primeiro offset usado
            "limit": 10,                      # O limite definido
            "total": total_vagas              # Total de vagas encontradas
        }
    }
    
# Salva as vagas encontradas em um arquivo JSON
    with open(SETTINGS["file_path"], "w", encoding="utf-8") as gupy:
        json.dump(todas_vagas, gupy, ensure_ascii=False, indent=2)

# Exibe o número de vagas encontradas e salva o arquivo
    print(f"\nTotal de vagas encontradas: {len(todas_vagas)}")

    return resultado