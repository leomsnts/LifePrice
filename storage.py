import json 
import os

PASTA_DADOS = "/tmp/data" if os.environ.get("VERCEL") else "data"

def carregar_json(caminho):
    if not os.path.exists(caminho):
        return None
    
    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return dados

def salvar_json(caminho, dados):
    pasta = os.path.dirname(caminho)
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta)

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=2, ensure_ascii=False)
        