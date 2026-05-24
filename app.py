from datetime import datetime

from flask import Flask, request, jsonify, render_template

from calculator import calcular_custo, gerar_frase
from profile import perfil_demo


app = Flask(__name__, static_folder="public", static_url_path="")



def msg(texto, tom="normal"):
    return {"tipo": "texto", "texto": texto, "tom": tom}


def tabela(titulo, linhas, cabecalho=None):
    return {"tipo": "tabela", "titulo": titulo, "cabecalho": cabecalho, "linhas": linhas}


def resultado_em_blocos(descricao, r, frase):
    linhas = [
        ["Preco", f"R$ {r['preco']:.2f}"],
        ["Valor da sua hora", f"R$ {r['valor_hora']:.2f}"],
        ["Horas de trabalho", f"{r['horas_trabalhadas']:.1f}h"],
        ["Dias uteis de trabalho", f"{r['dias_uteis']:.1f} dias"],
        ["Dias de vida acordado", f"{r['dias_de_vida_acordado']:.1f} dias"],
    ]
    return [tabela(f"Compra: {descricao}", linhas), {"tipo": "painel", "texto": frase}]


def perfil_em_blocos(p, titulo="Seu Perfil Financeiro"):
    linhas = [
        ["Salario mensal", f"R$ {p['salario_mensal']:.2f}"],
        ["Horas por dia", f"{p['horas_por_dia']}h"],
        ["Dias por mes", f"{p['dias_por_mes']} dias"],
        ["Horas de sono por dia", f"{p['horas_dormidas']}h"],
    ]
    return [tabela(titulo, linhas)]


def montar_demo():
    perfil = perfil_demo()

    blocos = [
        msg("MODO DEMONSTRAÇÃO"),
        msg("Usando perfil de exemplo: R$ 4.000 mensais, carga horária de trabalho de 8h/dia, 8h de sono, 22 dias úteis no mês.", "dim"),
    ]
    blocos += perfil_em_blocos(perfil)

    exemplos = [
        ("iPhone 17 Pro Max", 12500.00),
        ("Tenis novo", 950.00),
        ("Ifood", 115.00),
        ("Claude MAX", 493.00),
    ]
    for nome, preco in exemplos:
        r = calcular_custo(preco, perfil)
        blocos += resultado_em_blocos(nome, r, gerar_frase(nome, r))

    return blocos


def texto_privacidade():
    return [
        msg("Nota de privacidade"),
        msg("Conforme a Lei Geral de Proteção de Dados (LGPD):", tom="dim"),
        msg("Os dados eventualmente informados pelo usuário nesta plataforma, que incluem salário, jornada de trabalho, horas, dias trabalhados e despesas: são utilizados exclusivamente para processamento local e execução dos cálculos, não sendo armazenados, comercializados, compartilhados ou utilizados para quaisquer finalidades secundárias."),
        msg("O LifePrice não utiliza cookies de rastreamento, identificadores de publicidade, perfilamento comportamental ou tecnologias destinadas à coleta de dados para fins comerciais."),
    ]


def valida_perfil(dados):
    try:
        salario = float(dados["salario_mensal"])
        horas_dia = float(dados["horas_por_dia"])
        dias_mes = float(dados["dias_por_mes"])
        sono = float(dados["horas_dormidas"])
    except (KeyError, TypeError, ValueError):
        return None, "Dados invalidos. Informe apenas numeros."

    if salario <= 0:
        return None, "O salario precisa ser maior que zero."
    if horas_dia <= 0 or horas_dia > 24:
        return None, "A carga horaria precisa estar entre 0 e 24 horas."
    if dias_mes <= 0 or dias_mes > 31:
        return None, "Os dias uteis precisam estar entre 1 e 31."
    if sono <= 0 or sono >= 24:
        return None, "As horas de sono precisam estar entre 0 e 24."

    if horas_dia > 24 - sono:
        return None, "A carga horaria nao pode ser maior que as horas acordadas (24 - sono)."

    perfil = {
        "salario_mensal": salario,
        "horas_por_dia": horas_dia,
        "dias_por_mes": dias_mes,
        "horas_dormidas": sono,
    }
    return perfil, None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/demo", methods=["POST"])
def api_demo():
    return jsonify({"blocos": montar_demo()})


@app.route("/api/privacidade", methods=["POST"])
def api_privacidade():
    return jsonify({"blocos": texto_privacidade()})


@app.route("/api/perfil", methods=["POST"])
def api_perfil():
    perfil, erro = valida_perfil(request.get_json(silent=True) or {})
    if erro:
        return jsonify({"blocos": [{"tipo": "erro", "texto": erro}]}), 400

    blocos = [msg("Perfil definido para esta sessao.", "ok")]
    blocos += perfil_em_blocos(perfil)
    blocos.append({"tipo": "botao", "texto": "Calcular despesa", "acao": "despesa"})
    return jsonify({"blocos": blocos})


@app.route("/api/despesa", methods=["POST"])
def api_despesa():
    dados = request.get_json(silent=True) or {}

    perfil, erro = valida_perfil(dados.get("perfil") or {})
    if erro:
        return jsonify({"blocos": [
            {"tipo": "erro", "texto": "Perfil invalido ou ausente."},
            {"tipo": "botao", "texto": "Criar perfil", "acao": "perfil"},
        ]}), 400

    try:
        preco = float(dados["preco"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"blocos": [{"tipo": "erro", "texto": "Valor invalido. Informe um numero."}]}), 400

    if preco <= 0:
        return jsonify({"blocos": [{"tipo": "erro", "texto": "O valor da despesa precisa ser maior que zero."}]}), 400

    descricao = dados.get("descricao") or "Item"
    r = calcular_custo(preco, perfil)
    frase = gerar_frase(descricao, r)

    registro = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "descricao": descricao,
        "preco": r["preco"],
        "horas_trabalhadas": round(r["horas_trabalhadas"], 2),
        "dias_uteis": round(r["dias_uteis"], 2),
        "dias_de_vida": round(r["dias_de_vida_acordado"], 2),
    }
    return jsonify({"blocos": resultado_em_blocos(descricao, r, frase), "registro": registro})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
