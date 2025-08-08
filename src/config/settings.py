total = 10
offset = 0 
for _ in range(0, total, 10):
    offset += 10
    
SETTINGS = {
    "file_path": "./data/vagas_gupy.json",
    "palavras_chave": ["dados"], 
    "offset": [0, total, 10]
}