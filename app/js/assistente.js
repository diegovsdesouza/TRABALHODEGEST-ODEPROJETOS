// R13 · Assistente de IA do escritório de projetos.
// Monta um resumo do projeto com os números calculados pelo sistema na data de corte e:
//  1) pergunta à IA (função do Netlify, chave fora do repositório); ou
//  2) se a IA não estiver configurada, responde pelo assistente local, com regras sobre os mesmos números.
import { dados, fmt, dataCorte } from './db.js';
import * as K from './calc.js';

export function contextoProjeto(db, d) {
  const lb = K.linhaDeBase(db); const pv = K.previsao(db, d, lb); const ev = K.valorAgregado(db, d, lb); const rk = K.riscos(db); const rs = K.reservas(db, d);
  const ct = K.contratos(db, d); const pr = K.produtividade(db, d); const ag = pv.agil;
  const cen = db.cenarios.map((c) => ({ id: c.id_cenario, nome: c.nome_cenario, ...K.cenario(db, [c.id_cenario], d) }));
  const diretos = db.backlog_itens.filter((b) => b.origem === 'PEDIDO_DIRETO' && (!b.data_criacao || b.data_criacao <= d));
  const nome = (i) => db.atividades.find((a) => a.id_atividade === i)?.nome_atividade || i;
  const andam = pv.cadeia.filter((i) => pv.ativ[i].situacao === 'EM_ANDAMENTO');
  const R = {
    prazo: `Término previsto pela rede (convenção 11): ${fmt.data(pv.termino)}; linha de base ${fmt.data(lb.termino)}; contrato 07/05/2027. Dias úteis além do contrato: ${pv.duAlemContrato} (custo do atraso R$ 50.100/du = ${fmt.rs(pv.custoAtraso)}). Cadeia que define a data: ${pv.cadeia.join(' → ')}. ${andam.map((i) => `${i} ${nome(i)} está em ${pv.ativ[i].avanco}% e termina em ${fmt.data(pv.ativ[i].termino)} (${pv.ativ[i].desvio >= 0 ? '+' : ''}${pv.ativ[i].desvio} du sobre a linha de base)`).join('; ')}. Fontes: tabelas 07, 08, 11 e 17.`,
    custo: `Valor agregado do projeto (convenções 4 a 7): VP ${fmt.rs(ev.projeto.vp)}, VA ${fmt.rs(ev.projeto.va)}, CR ${fmt.rs(ev.projeto.cr)}; IDC ${fmt.n(ev.projeto.idc, 3)}, IDP ${fmt.n(ev.projeto.idp, 3)}; ENT = ONT ÷ IDC = ${fmt.rs(ev.projeto.ent)} (ONT ${fmt.rs(ev.projeto.ont)}, desvio ${fmt.rs(ev.projeto.ent - ev.projeto.ont)}); IDPT ${fmt.n(ev.projeto.idpt, 2)}. Entregas com IDC abaixo de 1: ${ev.entregas.filter((e) => e.idc != null && e.idc < 1).map((e) => `${e.entrega} (IDC ${fmt.n(e.idc, 3)}, VC ${fmt.rs(e.vcusto)})`).join('; ')}. Pagamentos acima do previsto: ${ct.filter((c) => c.desvioPago > 1000).map((c) => `${c.id_contrato} ${c.fornecedor} +${fmt.rs(c.desvioPago)}`).join('; ')}. Fontes: tabelas 09, 17, 18, 19 e 31.`,
    escopo: `Escopo sem controle de mudança: ${diretos.length} itens de origem PEDIDO_DIRETO, ${diretos.reduce((s, b) => s + Number(b.pontos), 0)} pontos, solicitados por ${[...new Set(diretos.map((b) => b.id_solicitante))].join(', ')} (montadora), sem solicitação de mudança: ${diretos.map((b) => b.id_item).join(', ')}. Mudanças formais em aberto: ${db.mudancas_solicitacoes.filter((m) => m.status === 'EM_ANALISE').map((m) => `${m.id_mudanca} ${m.descricao} (${fmt.rs(m.impacto_custo_rs)}, ${m.impacto_prazo_du} du)`).join('; ') || 'nenhuma'}. Fontes: tabelas 14, 20 e 28.`,
    fornecedores: `Contratos com multa por atraso (convenção 14): ${ct.filter((c) => c.multa > 0).map((c) => `${c.id_contrato} ${c.fornecedor}: ${c.atrasoUltimoMarco} dias, ${fmt.rs(c.multa)}`).join('; ') || 'nenhum'}. Contratação em aberto (comissionamento, convenção 15): ${K.selecaoFornecedor(db).slice(0, 3).map((p) => `${p.id_proposta} ${p.fornecedor} nota ${fmt.n(p.nota, 3)}`).join('; ')}. Fontes: tabelas 30, 31 e 32.`,
    riscos: `Exposição a riscos (convenção 12): ${fmt.rs(rk.exposicao)} em ${rk.abertas.length} ameaças abertas (maiores: ${rk.abertas.slice(0, 3).map((r) => `${r.id_risco} ${r.descricao} ${fmt.rs(r.vme)}`).join('; ')}). Contingência: ${fmt.rs(K.P.contingencia)}, já consumidos ${fmt.rs(rs.contingenciaUsada)} por ocorrências (saldo ${fmt.rs(rs.contingenciaSaldo)}). Reserva gerencial: ${fmt.rs(K.P.gerencial)}, consumidos ${fmt.rs(rs.gerencialUsada)}. Fontes: tabelas 26 e 27.`,
    agil: `Trilha ágil (convenções 8 e 10): velocidade média ${fmt.n(ag.vmed, 1)} pontos/sprint (${ag.ult5.map((s) => `${s}=${ag.vel[s] || 0}`).join(', ')}). Release 2: ${ag.releases.R2.pontosRestantes} pontos restantes, prevista para ${fmt.data(ag.releases.R2.data)} (planejada ${fmt.data(ag.releases.R2.planejada)}). Release 3: prevista para ${fmt.data(ag.releases.R3.data)}. O teste de aceite em campo (A47) depende da Release 2; o aceite final (A56) da Release 3. Fontes: tabelas 14, 15, 16 e 20.`,
    pessoas: `Produtividade (convenção 20): ${pr.filter((p) => p.semanas).map((p) => `${p.id_atividade} ${p.servico}: índice de produtividade ${fmt.n(p.indProd, 2)}, índice de efetivo ${fmt.n(p.indEfetivo, 2)}, duração restante ${p.duracaoRestante ?? '—'} du (${p.diagnostico})`).join('; ')}. Fontes: tabelas 41 e 42.`,
    cenarios: `Cenários (convenções 21 a 23; resultado = VPL − custo do atraso): ${cen.map((c) => `${c.id} ${c.nome}: término ${fmt.data(c.termino)}, ENT ${fmt.rs(c.ent)}, VPL ${fmt.rs(c.vpl)}, resultado ${fmt.rs(c.resultado)}`).join('; ')}. Maior resultado: ${cen.slice().sort((a, b) => b.resultado - a.resultado)[0].id}. Fontes: tabelas 02 e 43 a 46.`,
  };
  return { R, texto: `Data de corte: ${fmt.data(d)}.\n` + Object.entries(R).map(([k, v]) => `[${k.toUpperCase()}] ${v}`).join('\n') };
}

const REGRAS = [
  ['prazo', /prazo|termin|quando|atras|data|cronograma|caminho|crític|injetora/i],
  ['custo', /cust|ent\b|or[cç]ament|desvio|idc|idp|valor agregado|dinheiro|gast/i],
  ['escopo', /escopo|pedido|mudan|montadora|sm-/i],
  ['fornecedores', /fornec|contrat|multa|propost|comissionamento/i],
  ['riscos', /risco|reserva|conting|exposi|amea/i],
  ['agil', /sprint|velocidade|release|backlog|ágil|agil|jira/i],
  ['pessoas', /pessoa|equipe|produtiv|efetivo|gente/i],
  ['cenarios', /cen[aá]rio|decis|recomend|decidir|vpl|c[1-6]\b/i],
];
function local(pergunta, R) {
  const achou = REGRAS.filter(([, re]) => re.test(pergunta)).map(([k]) => R[k]);
  return achou.length ? achou.join('\n\n') : 'Posso responder sobre: prazo e caminho crítico, custo e valor agregado, escopo e mudanças, fornecedores e contratos, riscos e reservas, trilha ágil, pessoas e produtividade e cenários. Tente, por exemplo: "o que define a data de término?" ou "a reserva cobre os riscos?".';
}

export async function paginaAssistente(alvo) {
  const db = await dados(); const d = dataCorte(); const ctx = contextoProjeto(db, d);
  alvo.innerHTML = `<h2>Assistente do escritório de projetos · corte em ${fmt.data(d)}</h2>
  <div class="cartao"><p class="nota">Pergunte em português. O assistente responde só com os números que o sistema calculou na data de corte (convenções oficiais), citando a fonte. Com a IA configurada no Netlify, a resposta é escrita pela IA; sem ela, o assistente local responde pelas mesmas regras.</p>
    <div class="linha">${['O que define a data de término?', 'De onde vem o desvio de custo?', 'A reserva cobre os riscos?', 'Que escopo entrou sem controle?', 'Qual cenário vocês recomendam?', 'Falta gente ou produtividade?'].map((q) => `<button class="sec sug">${q}</button>`).join('')}</div>
    <form id="fq" class="linha" style="margin-top:8px"><input id="q" style="flex:1;min-width:240px" placeholder="Ex.: quanto vai custar o projeto?"><button>Perguntar</button></form>
    <div id="conversa" style="margin-top:10px"></div>
    <details style="margin-top:10px"><summary class="nota">Ver o contexto enviado à IA (números do sistema)</summary><pre style="white-space:pre-wrap;font-size:11px">${ctx.texto}</pre>
      <button class="sec" id="copiar">Copiar contexto</button></details></div>`;
  const conv = alvo.querySelector('#conversa');
  const perguntar = async (q) => {
    if (!q.trim()) return;
    const bloco = document.createElement('div'); bloco.className = 'cartao'; bloco.style.marginTop = '8px';
    bloco.innerHTML = `<b>Você:</b> ${q}<br><span class="nota">pensando…</span>`; conv.prepend(bloco);
    let resp = null, origem = 'assistente local';
    try {
      const r = await fetch('/.netlify/functions/assistente', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ pergunta: q, contexto: ctx.texto }) });
      if (r.ok) { const j = await r.json().catch(() => ({})); if (j.resposta) { resp = j.resposta; origem = 'IA (' + (j.modelo || 'Gemini') + ')'; } }
    } catch (e) { /* sem função: segue o local */ }
    if (!resp) resp = local(q, ctx.R);
    bloco.innerHTML = `<b>Você:</b> ${q}<p style="white-space:pre-wrap;margin:6px 0">${resp.replace(/</g, '&lt;')}</p><p class="fonte">Respondido por: ${origem} · números do sistema em ${fmt.data(d)}</p>`;
  };
  alvo.querySelector('#fq').onsubmit = (ev) => { ev.preventDefault(); const q = alvo.querySelector('#q').value; alvo.querySelector('#q').value = ''; perguntar(q); };
  alvo.querySelectorAll('.sug').forEach((b) => (b.onclick = () => perguntar(b.textContent)));
  alvo.querySelector('#copiar').onclick = () => navigator.clipboard?.writeText(ctx.texto);
}
