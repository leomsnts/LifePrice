import argparse

from profile import criar_perfil_interativo, carregar_perfil, perfil_demo
from calculator import calcular_custo, gerar_frase
from history import adicionar_ao_historico, listar_historico
from display import mostrar_resultado, mostrar_historico, mostrar_perfil

def comando_criar_perfil():
    criar_perfil_interativo()

def comando_calcular(preco, descricao):
    perfil = carregar_perfil()

    if perfil is None:
        print("Você ainda não criou um perfil.")
        print("Rode: python main.py criar-perfil")
        return

    resultado = calcular_custo(preco, perfil)
    frase = gerar_frase(descricao, resultado)
    mostrar_resultado(descricao, resultado, frase)
    adicionar_ao_historico(descricao, resultado)

def comando_historico():
    compras = listar_historico()
    mostrar_historico(compras)

def comando_demo():
    print("\n=== DEMONSTRAÇÃO (CENÁRIO FICTÍCIO) ===")
    print("Usando perfil de exemplo: R$ 4.000/mes, 8h/dia, 22 dias/mes\n")

    perfil = perfil_demo()
    mostrar_perfil(perfil)

    exemplos = [
        ("iPhone 17 Pro Max", 12500.00),
        ("Tenis novo", 950.00),
        ("Ifood", 115.00),
        ("Claude MAX", 493.00),
    ]

    for descricao, preco in exemplos:
        resultado = calcular_custo(preco, perfil)
        frase = gerar_frase(descricao, resultado)
        mostrar_resultado(descricao, resultado, frase)
        print()

def main():
    parser = argparse.ArgumentParser(
        description="LifePrice - Quanto isso custa em horas da sua vida?"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Roda o modo demonstracao com dados de exemplo",
    )

    subparsers = parser.add_subparsers(dest="comando")

    subparsers.add_parser("criar-perfil", help="Cria seu perfil financeiro")

    parser_calc = subparsers.add_parser("calcular", help="Calcula o custo de um item")
    parser_calc.add_argument(
        "--preco", type=float, required=True, help="Preco do item em R$"
    )
    parser_calc.add_argument(
        "--descricao", type=str, default="Item", help="Nome/descricao do item"
    )

    subparsers.add_parser("historico", help="Mostra o historico de compras")

    args = parser.parse_args()

    if args.demo:
        comando_demo()
        return

    if args.comando == "criar-perfil":
        comando_criar_perfil()
    elif args.comando == "calcular":
        comando_calcular(args.preco, args.descricao)
    elif args.comando == "historico":
        comando_historico()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()