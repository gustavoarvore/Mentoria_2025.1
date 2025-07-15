#Biblioteca para buscar vagas de emprego na Gupy
import requests
import json
import os

from config.settings import SETTINGS

# Função para buscar vagas na Gupy
# Faz uma requisição para a API da Gupy com as palavras-chave e offsets definidos
def buscar_vagas():
    todas_vagas = []
    os.makedirs(os.path.dirname(SETTINGS["file_path"]), exist_ok=True)

    for palavra in SETTINGS["palavras_chave"]:
        print(f"\nBuscando vagas para: {palavra}")

# Itera sobre os offsets para buscar todas as vagas disponíveis
        for offset in SETTINGS["offsets"]:
            url = f'https://portal.api.gupy.io/api/job?name={palavra}&offset={offset}&limit=10'
            resposta = requests.get(url)
            if resposta.status_code != 200:
                print(f"Erro ao buscar vagas: {resposta.status_code}")
                continue

# Processa a resposta JSON e extrai as vagas
            dados = resposta.json()
            vagas = dados.get("data", [])

            todas_vagas.extend(vagas)

# Salva as vagas encontradas em um arquivo JSON
    if not todas_vagas:
        print("Nenhuma vaga encontrada.")
        return
    with open(SETTINGS["file_path"], "w", encoding="utf-8") as gupy:
        json.dump(todas_vagas, gupy, ensure_ascii=False, indent=2)

# Exibe o número de vagas encontradas e salva o arquivo
    print(f"\nTotal de vagas encontradas: {len(todas_vagas)}")
buscar_vagas()