from storage import carregar_json, salvar_json, PASTA_DADOS

CAMINHO_PERFIL = f"{PASTA_DADOS}/perfil.json"

def criar_perfil_interativo():
    print("\n=== Vamos criar seu perfil financeiro ===\n")

    salario = float(input("Informe seu salário líquido: "))
    horas_por_dia = float(input("Informe sua carga horária: "))
    dias_por_mes = float(input("Informe os dias uteis deste mês: "))
    horas_dormidas = float(input("Informe quanto tempo você costuma dormir (horas/dia): "))

    perfil = {
        "salario_mensal": salario,
        "horas_por_dia": horas_por_dia,
        "dias_por_mes": dias_por_mes,
        "horas_dormidas": horas_dormidas,
    }

    salvar_json(CAMINHO_PERFIL, perfil)
    print(print("\nSeu perfil foi salvo! Agora você precisa informar o preço e a descrição do item/despesa que você quer calcular.\n"))
    print(print("\nInforme pra mim neste comando: python main.py calcular --preco (valor) --descricao (item/despesa, em aspas)\n"))
    return perfil

def carregar_perfil():
    return carregar_json(CAMINHO_PERFIL)

def perfil_demo():
    return {
        "salario_mensal": 4000.00,
        "horas_por_dia": 8,
        "dias_por_mes": 22,
        "horas_dormidas": 8,
    }