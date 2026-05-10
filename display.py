"""Formatação da saída no terminal. Usa a biblioteca 'rich' se estiver instalado, caso contrário, cai no print() simples."""

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    USAR_RICH = True
    console = Console()
except ImportError:
    USAR_RICH = False
    console = None

#Acima contém o padrão de import opcional. A bibliotecha 'rich' é externa, precisa de pip install.
#Se o usuário optar por não instalar o 'rich', o Try tenta executar o que está dentro. Se algo falhar, o except captura o erro e continua.
#USAR_RICH = True é a variável global para indicar para usar o 'rich'
#console = Console() serve para criar o objeto Console que vamos usar em várias funções.
#USAR_RICH = False marca que não tem rich.
#No final de tudo, quem instala o 'rich' vê as tabelas coloridas, quem não instalar vê texto puro... e o programa não vai quebrar.

def mostrar_resultado(descricao, resultado, frase):
    """Mostra o resultado de um cálculo."""
    if USAR_RICH:
        _mostrar_resultado_rich(descricao, resultado, frase)
    else:
        _mostrar_resultado_simples(descricao, resultado, frase)
#Essa função decide qual versão chamar, se o usuário instalar ou não o 'rich'.

def _mostrar_resultado_rich(descricao, resultado, frase):
    tabela = Table(title=f"Compra: {descricao}", show_header=False)
    #Cria um objeto Table do 'rich'. O show_header=False esconde os nomes das colunas.
    tabela.add_column("Metrica", style="cyan")
    #Adiciona coluna estilizada na cor ciano.
    tabela.add_column("Valor", style="yellow")
    #Adiciona outra coluna em amarelo.

    tabela.add_row("Preco", f"R$ {resultado['preco']:.2f}")
    #Adiciona linha com dois valores, e formata o número com 2 casas decimais e prefixa o R$.
    tabela.add_row("Valor da sua hora", f"R$ {resultado['valor_hora']:.2f}")
    tabela.add_row("Horas de trabalho", f"{resultado['horas_trabalhadas']:.1f}h")
    tabela.add_row("Dias uteis de trabalho", f"{resultado['dias_uteis']:.1f} dias")
    tabela.add_row("Dias de vida acordado", f"{resultado['dias_de_vida_acordado']:.1f} dias")

    console.print(tabela)
    #Manda a tabela para o terminal. O 'rich' cuida de renderizar com cores e bordas.
    console.print(Panel(frase, style="bold red"))
    #Desenha um quadro vermelho em volta da frase. O usuário SEMPRE verá ela.

def _mostrar_resultado_simples(descricao, resultado, frase):
#Versão sem o 'rich'.
    print(f"\n=== Custo Real: {descricao} ===")
    print(f"Preco:                  R$ {resultado['preco']:.2f}")
    print(f"Valor da sua hora:      R$ {resultado['valor_hora']:.2f}")
    print(f"Horas de trabalho:      {resultado['horas_trabalhadas']:.1f}h")
    print(f"Dias uteis de trabalho: {resultado['dias_uteis']:.1f} dias")
    print(f"Dias de vida acordado:  {resultado['dias_de_vida_acordado']:.1f} dias")
    print(f"\n>>> {frase}\n")

def mostrar_historico(compras):
    """Mostra o histórico de compras como tabela."""
    if len(compras) == 0:
        print("Nenhuma compra no historico ainda.")
        return
    
    if USAR_RICH:
        tabela = Table(title="Historico de Compras Analisadas")
        tabela.add_column("Data", style="dim")
        tabela.add_column("Descricao", style="cyan")
        tabela.add_column("Preco", style="yellow", justify="right")
        tabela.add_column("Horas", justify="right")
        tabela.add_column("Dias uteis", justify="right")
        tabela.add_column("Dias de vida", style="red", justify="right")

        for compra in compras:
        #Loop sobre a lista, cada iteração, compra é um dicionário.
            tabela.add_row( #Adiciona uma linha por compra.
                compra["data"],
                compra["descricao"],
                f"R$ {compra['preco']:.2f}",
                f"{compra['horas_trabalhadas']:.1f}",
                f"{compra['dias_uteis']:.1f}",
                f"{compra['dias_de_vida']:.1f}",
            )
        console.print(tabela)
    else:
        print("\n=== Historico de Compras ===\n")
        for compra in compras:
            print(f"[{compra['data']}] {compra['descricao']}")
            print(f"  R$ {compra['preco']:.2f} = {compra['dias_de_vida']:.1f} dias de vida\n")

def mostrar_perfil(perfil):
    """Mostra o perfil financeiro do usuario."""
    if USAR_RICH:
        tabela = Table(title="Seu Perfil Financeiro", show_header=False)
        tabela.add_column("Item", style="cyan")
        tabela.add_column("Valor", style="yellow")

        tabela.add_row("Salario mensal", f"R$ {perfil['salario_mensal']:.2f}")
        tabela.add_row("Horas por dia", f"{perfil['horas_por_dia']}h")
        tabela.add_row("Dias por mes", f"{perfil['dias_por_mes']} dias")
        tabela.add_row("Horas acordado por dia", f"{perfil['horas_acordado_por_dia']}h")
        console.print(tabela)
    else:
        print("\n=== Seu Perfil Financeiro ===")
        print(f"Salario mensal:         R$ {perfil['salario_mensal']:.2f}")
        print(f"Horas por dia:          {perfil['horas_por_dia']}h")
        print(f"Dias por mes:           {perfil['dias_por_mes']} dias")
        print(f"Horas acordado por dia: {perfil['horas_acordado_por_dia']}h\n")