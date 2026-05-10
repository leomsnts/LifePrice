# LifePrice

O LifePrice é uma ferramenta de linha de comando que, com base no seu salário, mostra quanto tempo da sua vida uma compra realmente custa. Ela calcula quantas horas, dias, semanas ou até anos de trabalho você precisa dedicar para pagar por um produto, uma despesa ou qualquer gasto.


>**Projeto educativo**: Toda a arquitetura do projeto está brevemente comentado. Esta foi uma decisão consciente do autor, que quer que o LifePrice sirva como material de estudo para quem está começando em Python e ainda não tem familiaridade com organização em módulos.

*Em meus projetos futuros, conforme as boas práticas, a arquitetura será autoexplicativa.*

---

## Demonstração

```
> python main.py calcular --preco 9000 --descricao "RTX 5080"

         Compra: RTX 5080
┌────────────────────────┬──────────────┐
│ Preço                  │ R$ 9000.00   │
│ Valor da sua hora      │ R$ 22.73     │
│ Horas de trabalho      │ 396.0h       │
│ Dias úteis de trabalho │ 49.5 dias    │
│ Dias de vida acordado  │ 24.8 dias    │
└────────────────────────┴──────────────┘

╭───────────────────────────────────────────────────╮
│ "RTX 5080" custa 3.5 semanas da sua vida acordado.│
╰───────────────────────────────────────────────────╯
```

---

## Como rodar

Necessário ter o python instalado. 

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/lifeprice.git
cd lifeprice

# 2. Instale a única dependência (opcional, mas recomendo para poder visualizar um menu mais bonito.)
pip install -r requirements.txt

# 3. Veja o projeto rodando com dados de exemplo
python main.py --demo
```

---

## Comandos 

**Modo demonstração** (usa um perfil fake e analisa 4 itens de exemplo):

```bash
python main.py --demo
```

**Criar seu perfil financeiro:**

```bash
python main.py criar-perfil
```

**Calcular o custo de um item:**

```bash
python main.py calcular --preco 4500 --descricao "Notebook novo"
```

**Ver o histórico de compras analisadas:**

```bash
python main.py historico
```

---

## Funcionalidades

- Criação de perfil financeiro em JSON
- Cálculo de custo em horas trabalhadas, dias úteis e dias de vida acordado
- Histórico automático de todas as consultas
- Saída formatada com tabelas coloridas (via `rich`)

---

## Tecnologias usadas

- **Python** (biblioteca padrão: `argparse`, `json`, `os`, `datetime`)
- **rich** (única dependência externa, opcional, para deixar o terminal bonito)
- **JSON** 

---

## Licença

Feito por **Leonardo M**

https://www.linkedin.com/in/leomsnts/
