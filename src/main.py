from datasources.gupy import buscar_vagas
from config.settings import SETTINGS

#Função definida para importar outra função de um arquivo já existente
def main():
    buscar_vagas(SETTINGS["palavras_chave"])

if __name__ == "__main__":
    main()
