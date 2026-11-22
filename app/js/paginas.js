// R4, R5, R6, R11 e conferência: páginas de leitura. Todos os números saem de calc.js com a data de corte do topo.
import Chart from 'chart.js/auto';
import { dados, fmt, htmlTabela, dataCorte } from './db.js';
import * as K from './calc.js';

const graficos = [];
function grafico(canvas, cfg) { const g = new Chart(canvas, cfg); graficos.push(g); return g; }
const limpar = () => { while (graficos.length) graficos.pop().destroy(); };
const kpi = (titulo, valor, sub = '', classe = '') => `<div class="kpi ${classe}"><small>${titulo}</small><b>${valor}</b><small>${sub}</small></div>`;
const mil = (v) => fmt.n(v / 1000, 1);

// ---------------- R11 · Dashboard
export async function paginaDashboard(alvo) {
  limpar(); const db = await dados(); const d = dataCorte(); const lb = K.linhaDeBase(db);
  const pv = K.previsao(db, d, lb); const ev = K.valorAgregado(db, d, lb); const rk = K.riscos(db); const rs = K.reservas(db, d); const ag = pv.agil; const pj = ev.projeto;
  const pedDir = db.backlog_itens.filter((b) => b.origem === 'PEDIDO_DIRETO' && (!b.data_criacao || b.data_criacao <= d));
  alvo.innerHTML = `<h2>Dashboard do comitê · corte em ${fmt.data(d)}</h2>
  <div class="kpis">
    ${kpi('Término previsto (rede)', fmt.data(pv.termino), `linha de base ${fmt.data(lb.termino)} · contrato 07/05/2027`, pv.duAlemContrato > 0 ? 'ruim' : 'bom')}
    ${kpi('Dias úteis além do contrato', pv.duAlemContrato, `custo do atraso ${fmt.rs(pv.custoAtraso)}`, pv.duAlemContrato > 0 ? 'ruim' : 'bom')}
    ${kpi('Estimativa no término (ENT)', fmt.mi(pj.ent), `ONT ${fmt.mi(pj.ont)} · desvio ${fmt.mi(pj.ent - pj.ont)}`, pj.ent > pj.ont ? 'ruim' : 'bom')}
    ${kpi('IDC / IDP do projeto', `${fmt.i(pj.idc)} / ${fmt.i(pj.idp)}`, `IDPT ${fmt.i(pj.idpt)}`, pj.idp < 0.95 ? 'ruim' : '')}
    ${kpi('Velocidade média (5 sprints)', fmt.n(ag.vmed, 1) + ' pt', `últimas: ${ag.ult5.map((s) => ag.vel[s] || 0).join(', ')}`)}
    ${kpi('Release 2 prevista', fmt.data(ag.releases.R2.data), `planejada ${fmt.data(ag.releases.R2.planejada)} · ${ag.releases.R2.pontosRestantes} pt restantes`, ag.releases.R2.data > ag.releases.R2.planejada ? 'ruim' : '')}
    ${kpi('Exposição a riscos (VME)', fmt.rs(rk.exposicao), `saldo da contingência ${fmt.rs(rs.contingenciaSaldo)} (consumidos ${fmt.rs(rs.contingenciaUsada)} de ${fmt.rs(K.P.contingencia)})`, rs.contingenciaSaldo < rk.exposicao ? 'ruim' : 'bom')}
    ${kpi('Pedidos diretos no backlog', pedDir.length + ' itens', `${pedDir.reduce((s, b) => s + b.pontos, 0)} pontos sem solicitação de mudança`, pedDir.length ? 'ruim' : '')}
  </div>
  <div class="grade">
    <div class="cartao"><h3>O que define a data hoje</h3><p>${pv.cadeia.map((i) => `<span class="chip ${pv.ativ[i].situacao === 'CONCLUIDA' ? 'ok' : 'crit'}">${i}</span>`).join(' → ')}</p>
      <p class="nota">${pv.cadeia.filter((i) => pv.ativ[i].situacao === 'EM_ANDAMENTO').map((i) => `${i} ${db.atividades.find((a) => a.id_atividade === i).nome_atividade} está em ${pv.ativ[i].avanco}% e termina em ${fmt.data(pv.ativ[i].termino)} (linha de base ${fmt.data(lb.ativ[i].termino)}).`).join(' ')}</p>
      <p class="fonte">Convenção 11 · tabelas 07, 08, 11, 17 e releases previstas pela velocidade (convenção 10).</p></div>
    <div class="cartao"><h3>Curva S do projeto (R$ mil)</h3><canvas id="gS" class="grafico"></canvas><p class="fonte">Convenções 4 a 6 · VP, VA e CR acumulados no fim de cada mês, duas frentes.</p></div>
  </div>`;
  curvaS(alvo.querySelector('#gS'), db, lb, d);
}

function curvaS(canvas, db, lb, ate) {
  const meses = []; for (let m = 2; m <= 30; m++) { const ano = 2026 + Math.floor((m - 1) / 12); const mm = ((m - 1) % 12) + 1;
    const fim = new Date(Date.UTC(ano, mm, 0)).toISOString().slice(0, 10); meses.push(fim); if (fim >= '2027-05-31') break; }
  const pts = meses.map((m) => K.valorAgregado(db, m, lb).projeto);
  const cort = (arr) => arr.map((v, i) => (meses[i] <= ate || meses[i - 1] < ate ? v : null));
  grafico(canvas, { type: 'line', data: { labels: meses.map((m) => m.slice(5, 7) + '/' + m.slice(2, 4)), datasets: [
    { label: 'VP', data: pts.map((p) => p.vp / 1000), borderColor: '#2f75b5', pointRadius: 0 },
    { label: 'VA', data: cort(pts.map((p) => p.va / 1000)), borderColor: '#2e7d32', pointRadius: 2 },
    { label: 'CR', data: cort(pts.map((p) => p.cr / 1000)), borderColor: '#c00000', pointRadius: 2 }] }, options: { plugins: { legend: { position: 'bottom' } } } });
}

// ---------------- R4 · Prazo: rede, caminho crítico e previsão
export async function paginaPrazo(alvo) {
  limpar(); const db = await dados(); const d = dataCorte(); const lb = K.linhaDeBase(db); const pv = K.previsao(db, d, lb);
  const nome = Object.fromEntries(db.atividades.map((a) => [a.id_atividade, a.nome_atividade]));
  const linhas = lb.ordem.map((i) => ({ id: i, nome: nome[i], dur: lb.dur[i], ...lb.ativ[i], prev: pv.ativ[i] })).sort((a, b) => a.ES - b.ES);
  const max = Math.max(pv.fim, lb.fim) + 5; const px = (du) => (du / max * 100).toFixed(2) + '%'; const st = lb.C.duAte(d);
  alvo.innerHTML = `<h2>Prazo · rede, caminho crítico e previsão em ${fmt.data(d)}</h2>
  <div class="kpis">${kpi('Linha de base', fmt.data(lb.termino), `du ${lb.fim}`)}${kpi('Previsão', fmt.data(pv.termino), `du ${pv.fim} · ${pv.desvioLb >= 0 ? '+' : ''}${pv.desvioLb} du`, pv.duAlemContrato > 0 ? 'ruim' : 'bom')}
    ${kpi('Folga até o contrato', -pv.duAlemContrato + ' du', 'contrato em 07/05/2027 (du 312)', pv.duAlemContrato > 0 ? 'ruim' : 'bom')}${kpi('Críticas na linha de base', linhas.filter((l) => l.critica).length + ' de ' + linhas.length)}</div>
  <div class="cartao"><h3>Gantt: linha de base (tracejado) × previsão (barra; vermelho = cadeia que define o término)</h3>
    <div class="gantt">${linhas.map((l) => `<div class="linha-g" title="${l.id} ${l.nome}"><span style="position:absolute;left:0;width:60px;font-size:11px">${l.id}</span>
      <div style="position:absolute;left:62px;right:0;top:4px;height:12px"><div class="barra lb" style="left:${px(l.ES - 1)};width:${px(l.dur)}"></div>
      <div class="barra ${l.prev.naCadeia ? 'crit' : ''}" style="left:${px(l.prev.ES - 1)};width:${px(l.prev.EF - l.prev.ES + 1)};opacity:.85"></div>
      <div class="status" style="left:${px(st)}"></div></div></div>`).join('')}</div>
    <p class="fonte">Linha verde = data de corte. Convenções 1, 2 e 11 · tabelas 07, 08, 11 e 17.</p></div>
  <div class="cartao" style="margin-top:12px"><h3>Tabela da rede</h3>${htmlTabela(linhas, [
    { campo: 'id', titulo: 'Ativ.', t: 1 }, { campo: 'nome', titulo: 'Atividade', t: 1 }, { campo: 'dur', titulo: 'Dur. (du)' },
    { campo: 'ES', titulo: 'IC' }, { campo: 'EF', titulo: 'TC' }, { campo: 'LS', titulo: 'IT' }, { campo: 'LF', titulo: 'TT' },
    { campo: 'folga', titulo: 'Folga', cor: (v) => (v === 0 ? 'neg' : '') },
    { campo: 'termino', titulo: 'Término LB', f: fmt.data }, { campo: 'prev', titulo: 'Situação', f: (v) => v.situacao.replace(/_/g, ' '), t: 1 },
    { campo: 'prev', titulo: 'Avanço', f: (v) => v.avanco + '%' }, { campo: 'prev', titulo: 'Término previsto', f: (v) => fmt.data(v.termino) },
    { campo: 'prev', titulo: 'Desvio (du)', f: (v) => v.desvio, cor: (v) => (v.desvio > 0 ? 'neg' : '') }])}</div>`;
}

// ---------------- R5 · Valor agregado
export async function paginaCusto(alvo) {
  limpar(); const db = await dados(); const d = dataCorte(); const lb = K.linhaDeBase(db); const ev = K.valorAgregado(db, d, lb);
  const linhas = [...ev.entregas, { ...ev.preditiva, total: 1 }, ev.agil, { ...ev.projeto, total: 1 }];
  const nomeE = Object.fromEntries(db.eap.map((e) => [e.codigo_eap, e.nome]));
  const pj = ev.projeto;
  alvo.innerHTML = `<h2>Valor agregado em ${fmt.data(d)}</h2>
  <div class="kpis">${kpi('VP', fmt.mi(pj.vp))}${kpi('VA', fmt.mi(pj.va))}${kpi('CR', fmt.mi(pj.cr))}
    ${kpi('IDC', fmt.i(pj.idc), 'VA ÷ CR', pj.idc < 1 ? 'ruim' : 'bom')}${kpi('IDP', fmt.i(pj.idp), 'VA ÷ VP', pj.idp < 1 ? 'ruim' : 'bom')}
    ${kpi('ENT = ONT ÷ IDC', fmt.mi(pj.ent), `ONT ${fmt.mi(pj.ont)}`)}${kpi('IDPT', fmt.i(pj.idpt), '(ONT − VA) ÷ (ONT − CR)')}</div>
  <div class="cartao">${htmlTabela(linhas, [
    { campo: 'entrega', titulo: 'Entrega', t: 1, f: (v) => (nomeE[v] ? `${v} ${nomeE[v]}` : v) }, { campo: 'ont', titulo: 'ONT (R$ mil)', f: mil },
    { campo: 'vp', titulo: 'VP', f: mil }, { campo: 'va', titulo: 'VA', f: mil }, { campo: 'cr', titulo: 'CR', f: mil },
    { campo: 'vprazo', titulo: 'VPr = VA − VP', f: mil, cor: (v) => (v < 0 ? 'neg' : '') }, { campo: 'vcusto', titulo: 'VC = VA − CR', f: mil, cor: (v) => (v < 0 ? 'neg' : '') },
    { campo: 'idp', titulo: 'IDP', f: (v) => (v == null ? '—' : fmt.n(v, 3)) }, { campo: 'idc', titulo: 'IDC', f: (v) => (v == null ? '—' : fmt.n(v, 3)), cor: (v) => (v != null && v < 1 ? 'neg' : '') }],
    { classeLinha: (l) => (l.total ? 'total' : '') })}
    <p class="fonte">VP: orçamento da tabela 09 distribuído pela duração da linha de base (convenção 4). VA: último avanço da tabela 17 × orçamento (5). CR: tabela 19 + horas da tabela 18 × custo/hora, extra × 1,5 (6). Ágil: sprints planejadas e pontos do escopo inicial concluídos.</p></div>
  <div class="cartao" style="margin-top:12px"><h3>Curva S (R$ mil)</h3><canvas id="gS" class="grafico"></canvas></div>`;
  curvaS(alvo.querySelector('#gS'), db, lb, d);
}

// ---------------- R6 · Painel ágil
export async function paginaAgil(alvo) {
  limpar(); const db = await dados(); const d = dataCorte(); const ag = K.agil(db, d); const C = K.calendario(db.calendario);
  const sprints = db.sprints.slice().sort((a, b) => a.numero - b.numero);
  const spSel = sessionStorage.getItem('spBurn') || ag.encerradas.at(-1) || 'S13';
  const bd = burndown(db, C, spSel); const fl = fluxo(db, C, spSel);
  const imps = db.implantacoes.filter((i) => i.data <= d && i.ambiente === 'PRODUCAO'); const sem = Math.max(1, K.diasCorridos('2026-05-04', d) / 7);
  const tempos = imps.map((i) => Number(i.tempo_ate_producao_h)).sort((a, b) => a - b); const med = tempos.length ? tempos[Math.floor((tempos.length - 1) / 2)] / 2 + tempos[Math.ceil((tempos.length - 1) / 2)] / 2 : null;
  const falhas = imps.filter((i) => Number(i.falhou) === 1);
  alvo.innerHTML = `<h2>Painel ágil · corte em ${fmt.data(d)}</h2>
  <div class="kpis">${kpi('Velocidade média', fmt.n(ag.vmed, 1) + ' pt/sprint', `${ag.ult5.join(', ')}`)}
    ${['R1', 'R2', 'R3'].map((r) => kpi(`${r} prevista`, fmt.data(ag.releases[r].data), `planejada ${fmt.data(ag.releases[r].planejada)} · faltam ${ag.releases[r].pontosRestantes} pt`, ag.releases[r].data > ag.releases[r].planejada ? 'ruim' : 'bom')).join('')}
    ${kpi('Itens / pontos concluídos', `${ag.itensConcluidos} / ${ag.pontosConcluidos}`)}
    ${kpi('DORA · frequência', fmt.n(imps.length / sem, 2) + '/sem', `lead time mediano ${fmt.n(med, 1)} h`)}
    ${kpi('DORA · falha / restauração', fmt.pct(falhas.length / (imps.length || 1)), `restauração média ${fmt.n(falhas.reduce((s, i) => s + Number(i.tempo_restauracao_h || 0), 0) / (falhas.length || 1), 1)} h`)}</div>
  <div class="grade">
    <div class="cartao"><h3>Velocidade por sprint (pontos)</h3><canvas id="gV" class="grafico"></canvas><p class="fonte">Convenção 8 · tabela 20, itens concluídos na sprint.</p></div>
    <div class="cartao"><h3>Burndown da sprint <select id="spB">${sprints.map((s) => `<option ${s.id_sprint === spSel ? 'selected' : ''}>${s.id_sprint}</option>`).join('')}</select></h3>
      <canvas id="gB" class="grafico"></canvas>
      <p class="nota">Velocidade ${bd.vel} pt · tempo de ciclo médio ${fmt.n(fl.ciclo, 1)} du · vazão ${fmt.n(fl.vazao, 2)} itens/du · WIP (Little) ${fmt.n(fl.vazao * fl.ciclo, 1)} itens</p>
      <p class="fonte">Restantes no fim de cada dia útil = pontos dos itens da sprint − pontos concluídos (M5). Ciclo: 1ª entrada em andamento até a conclusão, contando os extremos (convenção 9).</p></div>
  </div>`;
  grafico(alvo.querySelector('#gV'), { type: 'bar', data: { labels: ag.encerradas, datasets: [{ label: 'pontos concluídos', data: ag.encerradas.map((s) => ag.vel[s] || 0), backgroundColor: '#2f75b5' }] }, options: { plugins: { legend: { display: false } } } });
  grafico(alvo.querySelector('#gB'), { type: 'line', data: { labels: bd.dias.map((x) => fmt.data(x).slice(0, 5)), datasets: [
    { label: 'restantes', data: bd.rest, borderColor: '#c00000' }, { label: 'ideal', data: bd.ideal, borderColor: '#6b7785', borderDash: [5, 4], pointRadius: 0 }] }, options: { plugins: { legend: { position: 'bottom' } } } });
  alvo.querySelector('#spB').onchange = (e) => { sessionStorage.setItem('spBurn', e.target.value); paginaAgil(alvo); };
}

export function burndown(db, C, sp) {
  const s = db.sprints.find((x) => x.id_sprint === sp); const itens = db.sprint_itens.filter((x) => x.id_sprint === sp);
  const dias = [...C.d2du.keys()].filter((x) => x >= s.data_inicio && x <= s.data_fim);
  const total = itens.reduce((a, x) => a + Number(x.pontos), 0); const bl = Object.fromEntries(db.backlog_itens.map((b) => [b.id_item, b]));
  const concl = itens.filter((x) => Number(x.concluido_na_sprint) === 1);
  const rest = dias.map((dd) => total - concl.filter((x) => bl[x.id_item]?.data_conclusao && bl[x.id_item].data_conclusao <= dd).reduce((a, x) => a + Number(x.pontos), 0));
  return { dias, rest, ideal: dias.map((_, i) => total * (1 - (i + 1) / dias.length)), total, vel: concl.reduce((a, x) => a + Number(x.pontos), 0) };
}

export function fluxo(db, C, sp) {
  const s = db.sprints.find((x) => x.id_sprint === sp);
  const concl = db.sprint_itens.filter((x) => x.id_sprint === sp && Number(x.concluido_na_sprint) === 1).map((x) => x.id_item);
  const ciclos = concl.map((id) => {
    const tr = db.itens_transicoes.filter((t) => t.id_item === id && t.status_destino === 'EM_ANDAMENTO').map((t) => t.data).sort();
    const fim = db.backlog_itens.find((b) => b.id_item === id)?.data_conclusao; if (!tr.length || !fim) return null;
    return C.duAte(fim) - C.duAte(tr[0]) + 1;
  }).filter((x) => x != null);
  const dus = C.duAte(s.data_fim) - C.duAte(s.data_inicio) + 1;
  return { ciclo: ciclos.reduce((a, b) => a + b, 0) / (ciclos.length || 1), vazao: concl.length / dus, n: concl.length };
}

// ---------------- R1 · Conferência com os números de controle e com o caderno
export async function paginaConferencia(alvo) {
  limpar(); const db = await dados(); const d = dataCorte();
  const c30 = K.controle(db, '2026-10-30'); const c13 = K.controle(db, '2026-11-13');
  const ok = (a, b) => (Math.abs(a - b) < 0.01 ? '<span class="ok">✔ confere</span>' : '<span class="erro">✘ diverge</span>');
  const linhas = c30.map((r, i) => ({ ...r, v13: c13[i].valor }));
  const lb = K.linhaDeBase(db); const ev = K.valorAgregado(db, '2026-09-25', lb).projeto;
  const sub = subredeM1(); const C = K.calendario(db.calendario); const bd = burndown(db, C, 'S13');
  alvo.innerHTML = `<h2>Conferência dos números de controle (dossiê, seção 3)</h2>
  <div class="cartao">${htmlTabela(linhas, [{ campo: 'indicador', titulo: 'Controle', t: 1 },
    { campo: 'esperado30', titulo: 'Esperado até 30/10', f: (v) => fmt.n(v, 2) }, { campo: 'valor', titulo: 'Sistema até 30/10', f: (v) => fmt.n(v, 2) }, { campo: 'valor', titulo: '', f: (v, l) => ok(v, l.esperado30) },
    { campo: 'esperado13', titulo: 'Esperado até 13/11', f: (v) => fmt.n(v, 2) }, { campo: 'v13', titulo: 'Sistema até 13/11', f: (v) => fmt.n(v, 2) }, { campo: 'v13', titulo: '', f: (v, l) => ok(v, l.esperado13) }])}
    <p class="fonte">A coluna de 13/11 só confere depois que todos os boletins B1 a B10 forem lançados pelas telas.</p></div>
  <h3 style="margin-top:16px">Conferência obrigatória com o caderno manuscrito</h3>
  <div class="cartao">${htmlTabela([
    { folha: 'M1 · prazo da sub-rede', sistema: sub.fim + ' du' },
    { folha: 'M1 · caminho crítico da sub-rede', sistema: sub.ordem.filter((i) => sub.ativ[i].critica).sort((a, b) => sub.ativ[a].ES - sub.ativ[b].ES).join(' → ') },
    { folha: 'M3 · VP / VA / CR do projeto em 25/09 (R$ mil)', sistema: `${mil(ev.vp)} / ${mil(ev.va)} / ${mil(ev.cr)}` },
    { folha: 'M3 · IDP / IDC do projeto em 25/09', sistema: `${fmt.n(ev.idp, 3)} / ${fmt.n(ev.idc, 3)}` },
    ...['C1', 'C3', 'C4'].map((c) => { const r = K.cenario(db, [c], '2026-11-13'); return { folha: `M7 · ${c}: término / ENT / VPL / payback / resultado`, sistema: `${fmt.data(r.termino)} / ${fmt.rs(r.ent)} / ${fmt.rs(r.vpl)} / ${fmt.n(r.payback, 2)} anos / ${fmt.rs(r.resultado)}` }; }),
    { folha: 'M5 · velocidade da S13 / burndown (pontos restantes no fim de cada dia)', sistema: `${bd.vel} pt / ${bd.rest.join(', ')}` },
  ], [{ campo: 'folha', titulo: 'Folha', t: 1 }, { campo: 'sistema', titulo: 'Sistema', t: 1 }])}
  <p class="fonte">O integrante compara com a própria folha. M7: a tabela do dossiê confere término e ENT (C1 41.764.252; C3 41.389.882; C4 42.969.789).</p></div>`;
}

// sub-rede da folha M1 (dossiê): 12 atividades, ligações com o resto do projeto retiradas
export function subredeM1() {
  const O = { A32: [32, 40, 56], A33: [23, 28, 39], A34: [3, 4, 6], A35: [20, 25, 45], A38: [19, 25, 38], A39: [18, 22, 37], A40: [14, 18, 30], A41: [5, 6, 9], A42: [12, 15, 21], A43: [9, 12, 17], A44: [4, 5, 10], A46: [9, 12, 22] };
  const dur = Object.fromEntries(Object.entries(O).map(([k, [o, m, p]]) => [k, Math.ceil((o + 4 * m + p) / 6 - 1e-9)]));
  const L = (p, s, t, d = 0) => ({ id_predecessora: p, id_sucessora: s, tipo_dependencia: t, defasagem_du: d });
  const dep = [L('A32', 'A33', 'II', 15), L('A32', 'A34', 'TI'), L('A33', 'A34', 'TI'), L('A33', 'A35', 'II', 10), L('A38', 'A40', 'II', 8), L('A39', 'A40', 'II', 8),
    L('A38', 'A41', 'TI'), L('A39', 'A41', 'TI'), L('A34', 'A42', 'TI'), L('A38', 'A42', 'TI'), L('A39', 'A42', 'TI'), L('A40', 'A43', 'TI'), L('A41', 'A43', 'TI'),
    L('A43', 'A44', 'TI'), L('A42', 'A46', 'TI'), L('A44', 'A46', 'TI'), L('A35', 'A46', 'TI')];
  return K.cpm(Object.keys(O), dur, dep);
}
