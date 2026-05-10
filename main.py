"""Ponto de entrada do programa (CLI)."""

import argparse
# O módilo argpase é uma ferramenta que transforma os argumentos da linha de comando em objetos Python. Sem ele, teriamos que ler manualmente e validar tudo na mão.

from profile import criar_perfil_interativo, carregar_perfil, perfil_demo
from calculator import calcular_custo, gerar_frase
from history import adicionar_ao_historico, listar_historico
from display import mostrar_resultado, mostrar_historico, mostrar_perfil

#Acima o main.py está importado funções específicas dos outros módulos do projeto. 

def comando_criar_perfil():
    """Cria um novo perfil financeiro de forma interativa."""
    criar_perfil_interativo()
    #criar_perfil_interativo() mora dentro do módulo profile.py.

def comando_calcular(preco, descricao):
    """Calcula o custo real de um item com base no perfil salvo."""
    perfil = carregar_perfil()

    if perfil is None:
    #Verificação de segurança. Se o usuário não criou o perfil, o programa não calcula nada. Não é correto usar == None, melhor usar is None.
        print("Você ainda não criou um perfil.")
        print("Rode: python main.py criar-perfil")
        return

    resultado = calcular_custo(preco, perfil)
    #Chama a função do módulo calculator.py, passando o preço e o perfil completo. Essa função devolve o dicionário com horas, dias úteis, dias de vida, valor da hora e etc.
    frase = gerar_frase(descricao, resultado)
    #Gera a frase, na qual o calculator.py é responsável.
    mostrar_resultado(descricao, resultado, frase)
    #Tudo passa para o display. 
    adicionar_ao_historico(descricao, resultado)
    #Registra a compra. O history.py vai cuidar de salvar isso no JSON. 

def comando_historico():
    """Mostra o histórico de compras analisadas."""
    #Mesma coisa, paga a lista de compras do history.py, manda para o display.py mostrar. O main.py não interpreta os dados, só faz a ponte. 
    compras = listar_historico()
    mostrar_historico(compras)

def comando_demo():
    """Roda o modo demonstração com um perfil e valores de exemplo."""
    print("\n=== DEMONSTRAÇÃO (CENÁRIO FICTÍCIO) ===")
    print("Usando perfil de exemplo: R$ 4.000/mes, 8h/dia, 22 dias/mes\n")

    perfil = perfil_demo()
    #Chama a função em profile.py que devolve um dicionário pré-pronto.
    mostrar_perfil(perfil)
    #Pede para o display.py mostrar o perfil de exemplo na tela.

    exemplos = [ #Aqui temos tuplas, são imutáveis. 
        ("iPhone 17 Pro Max", 12500.00),
        ("Tenis novo", 950.00),
        ("Ifood", 115.00),
        ("Claude MAX", 493.00),
    ]

    for descricao, preco in exemplos:
    #Esse for é um unpacking da tupla anterior. 
        resultado = calcular_custo(preco, perfil)
        frase = gerar_frase(descricao, resultado)
        mostrar_resultado(descricao, resultado, frase)
        print()

def main():
    parser = argparse.ArgumentParser(
        description="LifePrice - Quanto isso custa em horas da sua vida?"
    )#Cria um objeto que vai gerenciar todos os argumentos. 
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Roda o modo demonstracao com dados de exemplo",
    )#Define um argumento flag. Quando o usuário digita --demo, esse argumento vira True. Quando ele não escreve, vira False. É o action que faz essas seleções.

    subparsers = parser.add_subparsers(dest="comando")
    #Cria o sistema de subcomandos. O dest="comando" significa que quando o usuário rodar python main.py calcular, dentro do objeto de argumentos vai existir args.comando = "calcular".

    subparsers.add_parser("criar-perfil", help="Cria seu perfil financeiro")
    #Registra o subcomando criar-perfil.

    parser_calc = subparsers.add_parser("calcular", help="Calcula o custo de um item")
    #Registra o subcomando calcular. Aqui vamos guardar ele em uma variável porque vamos adicionar argumentos a ele. 
    parser_calc.add_argument(
        "--preco", type=float, required=True, help="Preco do item em R$"
    )#Adiciona o argumento --preco. O type=float faz o argparse converter automaticamente a string que o usuário digita em número decimal. O required=True significa que o programa dá erro se faltar. O help é a descrição que aparece no --help.
    parser_calc.add_argument(
        "--descricao", type=str, default="Item", help="Nome/descricao do item"
    )#Adiciona o argumento -descricao. Tem default="Item", ou seja, se o usuário esquecer, vai usar "Item" como padrão. 

    subparsers.add_parser("historico", help="Mostra o historico de compras")
    #Registra o subcomando historico, sem nenhum argumento.

    args = parser.parse_args()
    #Aqui lê o que o usuário digitou no terminal e devolve um objeto com tudo organizado.

    if args.demo:
    #Se a flag --demo foi usada, roda o modo demo e retorna imediatamente. 
        comando_demo()
        return

    if args.comando == "criar-perfil":
        comando_criar_perfil()
        #Se o comando for "criar-perfil", chama a função dela.
    elif args.comando == "calcular":
        comando_calcular(args.preco, args.descricao)
        #Se for o comando "calcular", chama a função passando o preço e a descrição que o usuário informou.
    elif args.comando == "historico":
        comando_historico()
        #Se for o comando "historico", chama a função dela, mostra o histórico.
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
    #Toda vez que o python é executado, ele define uma variável especial chamada __name__. E se o arquivo está sendo rodado diretamente (pyhton main.py), __name__ recebe o valor "__main__". Se o arquivo esta sendo importado por outro arquivo, __name__ recebe o nome do módulo ("main").
    #A condição if __name__ == "__main__" significa que, pra executar o código se o arquivo está sendo rodado diretamente, não se está sendo importado.
    #Isso permite que outros arquivos importem funções deste arquivo sem disparar a execução completa do programa. 
    #Serve como uma proteção contra erros durante imports. 