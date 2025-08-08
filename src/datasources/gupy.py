import requests
import json
import os

from config.settings import SETTINGS
from typing import Dict

Json = Dict[str, str]

def buscar_vagas(vaga: str) -> Json:
    if not isinstance(vaga, str):
        return print("A palavra-chave deve ser uma string.")
    
    todas_vagas = []
    SETTINGS["file_path"] = os.path.join("data", "vagas_gupy.json")
    os.makedirs(os.path.dirname(SETTINGS["file_path"]), exist_ok=True)

    for palavra in SETTINGS["palavras_chave"]:
        print(f"\nBuscando vagas para: {palavra}")

        for offset in SETTINGS["offset"]:
            url = f'https://portal.api.gupy.io/api/job?name={vaga}&offset={offset}&limit=10'
            resposta = requests.get(url)
            if resposta.status_code == 200:
                dados = resposta.json()
                
                if "data" in dados:
                    print(f"Vagas encontradas: {len(dados['data'])}")
                    todas_vagas.extend(dados.get("data", []))

    total_vagas = len(todas_vagas)
    resultado = {
        "data": todas_vagas,
        "pagination": {
            "offset": SETTINGS["offset"][0],  # Use o primeiro offset usado
            "limit": 10,                       # O limite definido
            "total": total_vagas               # Total de vagas encontradas
        }
    }
    
    with open(SETTINGS["file_path"], "w", encoding="utf-8") as gupy:
        json.dump(resultado, gupy, ensure_ascii=False, indent=2) 

    print(f"\nTotal de vagas encontradas: {total_vagas}")

    return resultado
