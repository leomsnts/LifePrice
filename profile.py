"""Criação e leitura do perfil do usuário, além da criação da versão --demo"""

from storage import carregar_json, salvar_json
#Pega as duas funções do storage.

CAMINHO_PERFIL = "data/perfil.json"
#É uma constante. 

def criar_perfil_interativo():
    """Pergunta os dados ao usuário e salva o perfil em JSON"""
    #Usamos JSON para salvar as poucas informações, usar banco de dados seria exagero.
    print("\n=== Vamos criar seu perfil financeiro ===\n")

    salario = float(input("Informe seu salário líquido: "))
    horas_por_dia = float(input("Informe sua carga horária: "))
    dias_por_mes = float(input("Informe os dias uteis deste mês: "))
    horas_acordado = float(input("Informe quantas horas por dia você fica acordado(a): "))

    perfil = {
        "salario_mensal": salario,
        "horas_por_dia": horas_por_dia,
        "dias_por_mes": dias_por_mes,
        "horas_acordado_por_dia": horas_acordado,
    }

    salvar_json(CAMINHO_PERFIL, perfil)
    #Delega o trabalho de gravação para o storage. Aqui, o profile.py não sabe como JSON funciona.
    print(print("\nSeu perfil foi salvo! Agora você precisa informar o preço e a descrição do item/despesa que você quer calcular.\n"))
    print(print("\nInforme pra mim neste comando: python main.py calcular --preco (valor) --descricao (item/despesa, em aspas)\n"))
    return perfil

#A criação do dicionário é a forma de estruturar os dados antes de gravar.
#Perceba que as chaves do dicionário são exatamente as mesmas que calculator.py.
#Criamos o dicionário com os dados, salvamos e retorna.

def carregar_perfil():
    """Lê o perfil salvo. Retorna None se ainda não existir."""
    return carregar_json(CAMINHO_PERFIL)
#O sistema não precisa saber que o perfil é salvo em JSON. Só precisa saber que tem a função de carregar perifl em profle.py.

def perfil_demo():
    """Retorna um perfil fixo para o modo demo."""
    return {
        "salario_mensal": 4000.00,
        "horas_por_dia": 8,
        "dias_por_mes": 22,
        "horas_acordado_por_dia": 16,
    }