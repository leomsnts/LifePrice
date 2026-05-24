from datetime import datetime
from storage import carregar_json, salvar_json, PASTA_DADOS

CAMINHO_HISTORICO = f"{PASTA_DADOS}/historico.json"

def carregar_historico():
    dados = carregar_json(CAMINHO_HISTORICO)
    if dados is None:
      return {"compras": []}
    return dados

def adicionar_ao_historico(descricao, resultado):
    historico = carregar_historico()

    nova_compra = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "descricao": descricao,
        "preco": resultado["preco"],
        "horas_trabalhadas": round(resultado["horas_trabalhadas"], 2),
        "dias_uteis": round(resultado["dias_uteis"], 2),
        "dias_de_vida": round(resultado["dias_de_vida_acordado"], 2),
    }

    historico["compras"].append(nova_compra)
    salvar_json(CAMINHO_HISTORICO, historico)


def listar_historico():
    historico = carregar_historico()
    return historico["compras"]