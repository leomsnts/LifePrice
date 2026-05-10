"""Funções simples para ler e gravar arquivos JSON"""

import json 
#Import da biblioteca padrão, módulo para ler/gravar JSON.
import os
#Imports da biblioteca padrão, módulo para mexer com o sistema de arquivos. (Verificar se arquivo existe, cria pastas e etc.)

def carregar_json(caminho):
    """Lê arquivo JSON. Retorna None se ele não existir."""
    if not os.path.exists(caminho):
        return None
    
    with open(caminho, "r", encoding="utf-8") as arquivo:
    #Nessa parte ele abre o arquivo em modo leitura ("r"), com codificação UTF-8, que suporta acentos.
        dados = json.load(arquivo)
        #Aqui ele lê o conteúdo do arquivo e converte para estruturas python (dicionários, listas, números, strings.) Então um JSON {"a": 1} vira o dicionário python {"a": 1}.
    return dados

def salvar_json(caminho, dados):
    """Salva um dicionário em arquivo JSON. Cria a pasta se precisar."""
    pasta = os.path.dirname(caminho)
    #Só extrai a parte da pasta do caminho se caminho = "data/perfil.json", então pasta = "data".
    if pasta and not os.path.exists(pasta):
    #Duas condições: Primeiro a string da pasta não está vazia (porque alguns arquivos são na raiz do projeto e não tem pasta); Segundo, a pasta não existe. Se ambas, vai criar. 
        os.makedirs(pasta)
        #Cria a pasta. Se a pasta tiver subpastas, cria todas de uma vez.

    with open(caminho, "w", encoding="utf-8") as arquivo:
    #Abre em modo escrita ("w") e substitui o arquivo se já existir.
        json.dump(dados, arquivo, indent=2, ensure_ascii=False)
        #Aqui converte os dados python para JSON e escreve no arquivo.
        #O indent=2 faz o JSON ficar indentado com 2 espaços, sem isso, sairia tudo numa linha.
        #O ensure_ascii=False permite que caracteres acentuados sejam salvos como eles mesmos.
        