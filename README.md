# LifePrice

O LifePrice é uma ferramenta que, com base no seu salário, mostra quanto tempo da sua vida e do seu trabalho árduo serão necessários para pagar uma despesa. 

Ela calcula quantas horas, dias, semanas ou até anos de trabalho você precisa dedicar para pagar por um produto, uma despesa ou qualquer gasto.

Acesse aqui: https://life-price.vercel.app/

---

## Como usar

A interação acontece pelo terminal da página, usando os atalhos da barra lateral — não é preciso decorar nenhum comando:

- **Criar perfil** — informe salário, carga horária, dias úteis e horas de sono. O perfil fica apenas no seu navegador, nesta sessão.
- **Calcular despesa** — informe o valor e a descrição para ver quanto aquela compra custa em horas, dias úteis e dias de vida acordado.
- **Ver demonstração** — mostra exemplos prontos com um perfil de amostra.
- **Histórico** — lista as compras já analisadas nesta sessão.
- **Privacidade** — exibe a nota de privacidade (LGPD).
- **Limpar** — apaga a conversa, mantendo as instruções iniciais.

---

## Tecnologias usadas

- **Python** (biblioteca padrão: `argparse`, `json`, `os`, `datetime`)
- **rich** (única dependência externa, opcional, para deixar o terminal bonito)
- **JSON** 

---

## Privacidade (LGPD)

Nada do que você digita fica salvo no servidor. O perfil e o histórico ficam só no seu navegador (sessionStorage) e somem quando você fecha a aba.

---

## Licença

Feito por **Leonardo M**

https://www.linkedin.com/in/leomsnts/
