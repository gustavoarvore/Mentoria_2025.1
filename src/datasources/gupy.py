import requests
import json
import os

from config.settings import SETTINGS
from typing import Dict

Json = Dict[str, str]

def buscando_valor_total() -> int:

    url = 'https://portal.api.gupy.io/api/job?name=dados&offset=0&limit=10'
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        return dados.get("pagination").get("total", 0)
    return 0

def buscar_vagas(vaga: str) -> Json:
    
    todas_vagas = []
    SETTINGS["file_path"] = os.path.join("data", "vagas_gupy.json")
    os.makedirs(os.path.dirname(SETTINGS["file_path"]), exist_ok=True)

    for palavra in SETTINGS["palavras_chave"]:
        print(f"\nBuscando vagas para: {palavra}")
        
        total = buscando_valor_total()
        offset = 0 
        for _ in range(0, total, 10):
    
            url = f'https://portal.api.gupy.io/api/job?name={vaga}&offset={offset}&limit=10'
            resposta = requests.get(url)
            if resposta.status_code != 200:
                break
            
            dados = resposta.json()
                
            if "data" in dados:
                print(f"Vagas encontradas: {len(dados['data'])}")
                todas_vagas.extend(dados.get("data", []))

            offset += 10
            
    
    with open(SETTINGS["file_path"], "w", encoding="utf-8") as gupy:
        json.dump(todas_vagas, gupy, ensure_ascii=False, indent=2) 
