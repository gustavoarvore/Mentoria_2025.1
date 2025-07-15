from config.settings import SETTINGS

# Configurações iniciais
# Define o caminho do arquivo e as palavras-chave para busca   
SETTINGS = {
    "file_path": "./data/vagas_gupy.json",
    "palavras_chave": input("Digite a vaga que deseja: ").split(","),
    "offsets": range(0, 200)  
}