// Terminal do LifePrice. Cuida do "chat" da tela, do assistente de perguntas
// e das chamadas pro backend. Perfil e historico ficam so no navegador.

const out = document.getElementById("term-output");
const form = document.getElementById("cmd-form");
const campo = document.getElementById("cmd-input");
const placeholderPadrao = "Use os atalhos para começar";

const K_PERFIL = "lifeprice-perfil";
const K_HIST = "lifeprice-historico";

function pegarPerfil() {
  try {
    const v = sessionStorage.getItem(K_PERFIL);
    return v ? JSON.parse(v) : null;
  } catch (e) {
    return null;
  }
}

function guardarPerfil(p) {
  try {
    sessionStorage.setItem(K_PERFIL, JSON.stringify(p));
  } catch (e) {}
}

function pegarHistorico() {
  try {
    const v = sessionStorage.getItem(K_HIST);
    return v ? JSON.parse(v) : [];
  } catch (e) {
    return [];
  }
}

function guardarNoHistorico(item) {
  try {
    const h = pegarHistorico();
    h.push(item);
    sessionStorage.setItem(K_HIST, JSON.stringify(h));
  } catch (e) {}
}

// perguntas que cada assistente faz, na ordem
const perguntasPerfil = [
  { chave: "salario_mensal", texto: "Informe seu salário:", numero: true },
  { chave: "horas_por_dia", texto: "Informe sua carga horária (horas/dia):", numero: true },
  { chave: "dias_por_mes", texto: "Informe os dias úteis deste mês:", numero: true },
  { chave: "horas_dormidas", texto: "Informe quanto tempo você costuma dormir (horas/dia):", numero: true },
];
const perguntasDespesa = [
  { chave: "preco", texto: "Informe o valor da despesa:", numero: true },
  { chave: "descricao", texto: "Informe o que é essa despesa:", numero: false },
];

let assistente = null; // guarda o estado quando a pessoa ta respondendo as perguntas
let typed = null;
let jaInteragiu = 0; // conta quantas vezes o chat foi atualizado

// no celular o layout muda (botoes em cima do input, teclado tapando o rodape)
function ehMobile() {
  return window.matchMedia("(max-width: 1023px)").matches;
}

function nova(tag, classe, texto) {
  const n = document.createElement(tag);
  if (classe) n.className = classe;
  if (texto !== undefined) n.textContent = texto;
  return n;
}

// No celular nao forco o foco, senao o teclado abre sozinho e atrapalha.
function focarInput() {
  if (!ehMobile()) campo.focus({ preventScroll: true });
}

// A 1a interacao deixa a pessoa onde ela esta (lendo a intro la em cima).
// Da 2a pra frente:
//   - desktop: a tela acompanha o rodape do chat
//   - celular: como o teclado tapa o rodape, trago o inicio do conteudo novo pro topo
function ajustaScroll(ancora) {
  jaInteragiu++;
  if (jaInteragiu < 2) return;
  if (ehMobile()) {
    out.scrollTop = ancora;
  } else {
    out.scrollTop = out.scrollHeight;
  }
}

function eco(texto) {
  const l = nova("div", "term-echo");
  l.appendChild(nova("span", "term-prompt-symbol", ">"));
  l.appendChild(document.createTextNode(" " + texto));
  out.appendChild(l);
}

function linha(texto, tom) {
  out.appendChild(nova("div", "term-line" + (tom && tom !== "normal" ? " " + tom : ""), texto));
}

function painel(texto) {
  out.appendChild(nova("div", "term-panel", texto));
}

function desenhaTabela(b) {
  const wrap = nova("div", "term-tablewrap");
  if (b.titulo) wrap.appendChild(nova("div", "term-tabletitle", b.titulo));

  const t = nova("table", "term-table");

  if (b.cabecalho) {
    const tr = nova("tr");
    b.cabecalho.forEach((h) => tr.appendChild(nova("th", null, h)));
    const thead = nova("thead");
    thead.appendChild(tr);
    t.appendChild(thead);
  }

  const corpo = nova("tbody");
  b.linhas.forEach((cols) => {
    const tr = nova("tr");
    cols.forEach((celula, i) => {
      const classe = b.cabecalho ? null : i === 0 ? "k" : "v";
      tr.appendChild(nova("td", classe, String(celula)));
    });
    corpo.appendChild(tr);
  });
  t.appendChild(corpo);

  wrap.appendChild(t);
  out.appendChild(wrap);
}

function desenhaBotao(b) {
  const wrap = nova("div", "term-botaowrap");
  const botao = nova("button", "term-botao");
  botao.type = "button";
  botao.appendChild(nova("i", "bi " + (b.acao === "perfil" ? "bi-person-gear" : "bi-cart3")));
  botao.appendChild(document.createTextNode(" " + b.texto));
  botao.onclick = function () {
    if (b.acao === "despesa") lpDespesa();
    else if (b.acao === "perfil") lpCriarPerfil();
  };
  wrap.appendChild(botao);
  out.appendChild(wrap);
}

function desenha(blocos) {
  const ancora = out.scrollHeight;
  (blocos || []).forEach(function (b) {
    if (b.tipo === "texto") linha(b.texto, b.tom);
    else if (b.tipo === "erro") linha(b.texto, "error");
    else if (b.tipo === "tabela") desenhaTabela(b);
    else if (b.tipo === "painel") painel(b.texto);
    else if (b.tipo === "botao") desenhaBotao(b);
    else if (b.tipo === "limpar") limpar();
  });
  ajustaScroll(ancora);
}

async function post(url, corpo) {
  const r = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(corpo || {}),
  });
  return { ok: r.ok, dados: await r.json() };
}

function mostrarHistorico() {
  const ancora = out.scrollHeight;
  const h = pegarHistorico();
  if (h.length === 0) {
    linha("Nenhuma compra no historico ainda.", "dim");
    ajustaScroll(ancora);
    return;
  }
  const cab = ["Data", "Descricao", "Preco", "Horas", "Dias uteis", "Dias de vida"];
  const linhas = h.map((c) => [
    c.data,
    c.descricao,
    "R$ " + Number(c.preco).toFixed(2),
    Number(c.horas_trabalhadas).toFixed(1),
    Number(c.dias_uteis).toFixed(1),
    Number(c.dias_de_vida).toFixed(1),
  ]);
  desenhaTabela({ titulo: "Historico de Compras Analisadas", cabecalho: cab, linhas: linhas });
  ajustaScroll(ancora);
}

function limpar() {
  out.innerHTML = "";
  jaInteragiu = 0;
  intro();
}

// ---- assistente de perguntas (perfil e despesa usam o mesmo motor) ----
function comecaAssistente(tipo, perguntas) {
  const ancora = out.scrollHeight;
  assistente = { tipo: tipo, perguntas: perguntas, respostas: {}, passo: 0 };
  linha(tipo === "perfil" ? "Criar perfil financeiro" : "Calcular o custo de uma despesa", "dim");
  linha("(digite 'cancelar' para sair)", "dim");
  pergunta();
  ajustaScroll(ancora);
}

// so escreve a pergunta atual; a rolagem fica por conta de quem chamou
function pergunta() {
  const p = assistente.perguntas[assistente.passo];
  linha(p.texto, "dim");
  campo.placeholder = p.texto;
  focarInput();
}

function fechaAssistente() {
  assistente = null;
  campo.placeholder = placeholderPadrao;
}

async function respondeAssistente(valor) {
  const ancora = out.scrollHeight;
  eco(valor);
  const v = valor.trim();

  if (v.toLowerCase() === "cancelar") {
    fechaAssistente();
    linha("Operacao cancelada.", "dim");
    ajustaScroll(ancora);
    return;
  }

  const p = assistente.perguntas[assistente.passo];

  if (p.numero) {
    const n = Number(v.replace(",", "."));
    if (v === "" || !isFinite(n)) {
      linha("Valor invalido. Informe um numero.", "error");
      pergunta();
      ajustaScroll(ancora);
      return;
    }
    assistente.respostas[p.chave] = n;
  } else {
    if (v === "") {
      linha("Digite uma descricao.", "error");
      pergunta();
      ajustaScroll(ancora);
      return;
    }
    assistente.respostas[p.chave] = v;
  }

  assistente.passo++;
  if (assistente.passo < assistente.perguntas.length) {
    pergunta();
    ajustaScroll(ancora);
    return;
  }

  // respondeu tudo, agora manda pro backend (o desenha() ja cuida da rolagem)
  const tipo = assistente.tipo;
  const respostas = assistente.respostas;
  fechaAssistente();

  if (tipo === "perfil") await enviaPerfil(respostas);
  else await enviaDespesa(respostas);
}

async function enviaPerfil(respostas) {
  try {
    const { ok, dados } = await post("/api/perfil", respostas);
    if (ok) guardarPerfil(respostas);
    desenha(dados.blocos);
  } catch (e) {
    linha("Erro ao falar com o servidor.", "error");
  }
}

async function enviaDespesa(respostas) {
  try {
    const { ok, dados } = await post("/api/despesa", {
      perfil: pegarPerfil(),
      preco: respostas.preco,
      descricao: respostas.descricao,
    });
    if (ok && dados.registro) guardarNoHistorico(dados.registro);
    desenha(dados.blocos);
  } catch (e) {
    linha("Erro ao falar com o servidor.", "error");
  }
}

form.addEventListener("submit", function (e) {
  e.preventDefault();
  const valor = campo.value;
  campo.value = "";

  if (assistente) {
    respondeAssistente(valor);
    return;
  }

  const t = valor.trim();
  if (t === "") return;

  // fora de um assistente nao tem o que fazer com texto solto, so dou uma dica
  const ancora = out.scrollHeight;
  eco(t);
  linha("Use os atalhos ao lado para começar.", "dim");
  ajustaScroll(ancora);
});

// clicar no terminal devolve o foco pro input no desktop; no celular nao (abriria o teclado)
out.addEventListener("mousedown", function () {
  if (ehMobile()) return;
  if (window.getSelection().toString()) return;
  setTimeout(function () {
    campo.focus({ preventScroll: true });
  }, 0);
});

const frasesIntro = [
  "Já se perguntou o quanto que tal despesa representa da sua renda mensal?",
  "Quanto tempo do seu trabalho árduo seria necessário para quitar uma compra/dívida? ",
  "Seus dados estão seguros.",
  "O LifePrice foi desenvolvido por linkedin.com/in/leomsnts/"
];

function intro() {
  const div = nova("div", "term-intro");
  const span = nova("span");
  span.id = "term-typed";
  div.appendChild(span);
  out.appendChild(div);

  if (typeof Typed !== "undefined") {
    if (typed) {
      try {
        typed.destroy();
      } catch (e) {}
    }
    typed = new Typed("#term-typed", {
      strings: frasesIntro,
      typeSpeed: 30,
      backSpeed: 15,
      backDelay: 2560,
      startDelay: 300,
      showCursor: true,
      loop: true,
    });
  } else {
    span.textContent = frasesIntro[0];
  }
}

// funcoes chamadas pelos botoes da barra lateral (e pelo botao da nota de privacidade)
function lpCriarPerfil() {
  if (assistente) fechaAssistente();
  comecaAssistente("perfil", perguntasPerfil);
}

function lpDespesa() {
  if (assistente) fechaAssistente();
  if (!pegarPerfil()) {
    desenha([
      { tipo: "erro", texto: "Você ainda não criou um perfil." },
      { tipo: "botao", texto: "Criar perfil", acao: "perfil" },
    ]);
    focarInput();
    return;
  }
  comecaAssistente("despesa", perguntasDespesa);
}

async function lpDemo() {
  if (assistente) fechaAssistente();
  try {
    const { dados } = await post("/api/demo");
    desenha(dados.blocos);
  } catch (e) {
    linha("Erro ao contatar o servidor.", "error");
  }
  focarInput();
}

function lpHistorico() {
  if (assistente) fechaAssistente();
  mostrarHistorico();
  focarInput();
}

async function lpPrivacidade() {
  if (assistente) fechaAssistente();
  try {
    const { dados } = await post("/api/privacidade");
    desenha(dados.blocos);
  } catch (e) {
    linha("Erro ao contatar o servidor.", "error");
  }
  focarInput();
}

function lpLimpar() {
  if (assistente) fechaAssistente();
  limpar();
  focarInput();
}

function abrirPrivacidade() {
  const alvo = document.getElementById("dashboard-container");
  if (alvo) alvo.scrollIntoView({ behavior: "smooth", block: "center" });
  setTimeout(lpPrivacidade, 500);
}

intro();
