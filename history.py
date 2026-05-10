"""Salva e lista o histórico de compras."""

from datetime import datetime
#Pega a classe datetime da bibioletca padrão, usaremos para registrar a hora de cada compra.
from storage import carregar_json, salvar_json

CAMINHO_HISTORICO = "data/historico.json"
#É uma constante.

def carregar_historico():
    """Lê o histórico do disco. Caso não existir, retorna estrutura vazia."""
    dados = carregar_json(CAMINHO_HISTORICO)
    if dados is None:
      #Esse padrão é um objeto nulo ou valor padrão seguro, ao invés de devolver nada, devolve uma versão vazia.
      return {"compras": []}
    return dados

def adicionar_ao_historico(descricao, resultado):
    """Adiciona uma compra ao historico e salva no JSON."""
    historico = carregar_historico()
    #Lê o histórico atual ou a estrutura vazia se não existir.

    nova_compra = {
    #Monta o dicionário da nova entrada.
        "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
        #"data" pega o momento atual e formata como string. Datatime.now() retorna um objeto datetime, .strftime converte para formato "2026-05-06 14:30"
        "descricao": descricao,
        "preco": resultado["preco"],
        "horas_trabalhadas": round(resultado["horas_trabalhadas"], 2),
        #Arredonda para 2 casas decimais. Isso evita que o JSON tenha números com 14 casas decimais.
        "dias_uteis": round(resultado["dias_uteis"], 2),
        "dias_de_vida": round(resultado["dias_de_vida_acordado"], 2),
    }

    historico["compras"].append(nova_compra)
    #Adiciona a nova compra à lista. O .append é o método das listas em python que adiciona um item ao final. 
    salvar_json(CAMINHO_HISTORICO, historico)
    #Grava tudo de volta. Nós lemos o histórico inteiro, adiciona uma entrada e regrafva o histórico inteiro. Para volumes pequenos isso serve, mas, para milhões de registros precisaremos usar um banco de dados. 


def listar_historico():
    """Retorna a lista de compras analisadas."""
    historico = carregar_historico()
    #Lê o histórico e devolve a lista de compras. 
    return historico["compras"]