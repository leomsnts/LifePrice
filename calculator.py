"""Lógica de cálculo do custo da despesa"""

def calcular_valor_hora(perfil):
    """Calcula quanto vale uma hora de trabalho do usuário."""
    horas_no_mes = perfil["horas_por_dia"] * perfil["dias_por_mes"]
    valor_hora = perfil["salario_mensal"] / horas_no_mes
    #O usuário preenche os dados pela chamada em profile.py
    return valor_hora

def calcular_custo(preco, perfil):
    """Calcula o custo de um item em horas e dias."""
    valor_hora = calcular_valor_hora(perfil)

    horas_trabalhadas = preco / valor_hora
    #Quantas horas você precisa trabalhar para pagar a despesa.
    dias_uteis = horas_trabalhadas / perfil["horas_por_dia"]
    #Converte horas em dias uteis dividindo pelas horas trabalhadas por dia.
    dias_de_vida = horas_trabalhadas / perfil["horas_acordado_por_dia"]
    #Converte para dias de vida acordado.

    resultado = {
        "preco": preco, 
        "valor_hora": valor_hora,
        "horas_trabalhadas": horas_trabalhadas,
        "dias_uteis": dias_uteis,
        "dias_de_vida_acordado": dias_de_vida,
    }
    return resultado
    #Devolve o dicionário completo.

def gerar_frase(descricao, resultado):
    """Gera a frase na unidade abaixo da tabela da análise financeira."""
    dias = resultado["dias_de_vida_acordado"]

    if dias < 1: 
        horas = resultado["horas_trabalhadas"]
        return f'"{descricao}" custa {horas:.1f} horas da sua vida acordado.'
    
    if dias < 7:
        return f'"{descricao}" custa {dias:.1f} dias da sua vida acordado.'

    if dias < 30:
        semanas = dias / 7
        return f'"{descricao}" custa {semanas:.1f} semanas da sua vida acordado.'

    if dias < 365:
        meses = dias / 30
        return f'"{descricao}" custa {meses:.1f} meses da sua vida acordado.'

    anos = dias / 365
    return f'"{descricao}" custa {anos:.1f} ANOS da sua vida acordado.'