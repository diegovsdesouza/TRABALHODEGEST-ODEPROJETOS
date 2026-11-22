// Núcleo de cálculo do sistema (convenções oficiais 1 a 23 do DICIONARIO.md).
// Funções puras: recebem as tabelas (arrays de objetos, como vêm do Supabase) e a data de corte.
// O mesmo arquivo roda no navegador e no Node (testes/teste_calc.mjs confere com o dossiê).

export const P = {
  inicio: '2026-02-02', contrato: '2027-05-07', status: '2026-11-13',
  ontPred: 38271476, ontAgil: 737800, contingencia: 831000, gerencial: 1170000,
  atrasoDu: 50100, tma: 0.14, fatorHE: 1.5, orcSprint: 43400,
};
const num = (v) => (v == null || v === '' ? null : Number(v));
const ceil = (x) => Math.ceil(x - 1e-9);
const addDias = (iso, d) => { const t = new Date(iso + 'T12:00:00Z'); t.setUTCDate(t.getUTCDate() + d); return t.toISOString().slice(0, 10); };
export const diasCorridos = (a, b) => Math.round((new Date(b + 'T12:00:00Z') - new Date(a + 'T12:00:00Z')) / 864e5);

// ---------- calendário: data <-> dia útil do projeto
export function calendario(cal) {
  const uteis = cal.filter((c) => c.dia_util_projeto != null).sort((a, b) => a.data.localeCompare(b.data));
  const d2du = new Map(uteis.map((c) => [c.data, Number(c.dia_util_projeto)]));
  const du2d = new Map(uteis.map((c) => [Number(c.dia_util_projeto), c.data]));
  const duAte = (iso) => { let n = 0; for (const c of uteis) { if (c.data <= iso) n = Number(c.dia_util_projeto); else break; } return n; };
  const fimSprint = {}; cal.forEach((c) => { if (c.id_sprint && (!fimSprint[c.id_sprint] || c.data > fimSprint[c.id_sprint])) fimSprint[c.id_sprint] = c.data; });
  return { d2du, du2d, duAte, fimSprint, data: (du) => du2d.get(du) };
}

// ---------- convenção 1: duração da linha de base
export function duracoes(atv) {
  const d = {};
  for (const a of atv) {
    d[a.id_atividade] = a.tipo_atividade === 'MARCO_AGIL' ? num(a.duracao_fixa_du)
      : ceil((num(a.duracao_otimista_du) + 4 * num(a.duracao_mais_provavel_du) + num(a.duracao_pessimista_du)) / 6);
  }
  return d;
}

// ---------- convenção 2: rede (ida e volta). dep: [{id_predecessora, id_sucessora, tipo_dependencia, defasagem_du}]
export function cpm(ids, dur, dep) {
  const preds = Object.fromEntries(ids.map((i) => [i, []])); const sucs = Object.fromEntries(ids.map((i) => [i, []]));
  for (const x of dep) {
    if (!(x.id_sucessora in preds) || !(x.id_predecessora in preds)) continue;
    const l = { p: x.id_predecessora, s: x.id_sucessora, t: x.tipo_dependencia, d: Number(x.defasagem_du) };
    preds[l.s].push(l); sucs[l.p].push(l);
  }
  const grau = Object.fromEntries(ids.map((i) => [i, preds[i].length])); const fila = ids.filter((i) => !grau[i]); const ordem = [];
  while (fila.length) { const i = fila.shift(); ordem.push(i); for (const l of sucs[i]) if (--grau[l.s] === 0) fila.push(l.s); }
  if (ordem.length !== ids.length) throw new Error('A rede tem ciclo');
  const ES = {}, EF = {}, LS = {}, LF = {};
  for (const i of ordem) {
    let es = 1; for (const l of preds[i]) es = Math.max(es, l.t === 'TI' ? EF[l.p] + 1 + l.d : ES[l.p] + l.d);
    ES[i] = es; EF[i] = es + dur[i] - 1;
  }
  const fim = Math.max(...ordem.map((i) => EF[i]));
  for (const i of [...ordem].reverse()) {
    let lf = fim; for (const l of sucs[i]) lf = Math.min(lf, l.t === 'TI' ? LS[l.s] - 1 - l.d : LS[l.s] - l.d + dur[i] - 1);
    LF[i] = lf; LS[i] = lf - dur[i] + 1;
  }
  const r = {}; for (const i of ids) r[i] = { ES: ES[i], EF: EF[i], LS: LS[i], LF: LF[i], dur: dur[i], folga: LS[i] - ES[i], critica: LS[i] === ES[i] };
  return { ativ: r, fim, ordem, preds };
}

export function linhaDeBase(db) {
  const C = calendario(db.calendario); const dur = duracoes(db.atividades);
  const ids = db.atividades.map((a) => a.id_atividade);
  const r = cpm(ids, dur, db.dependencias);
  for (const i of ids) { r.ativ[i].inicio = C.data(r.ativ[i].ES); r.ativ[i].termino = C.data(r.ativ[i].EF); }
  r.termino = C.data(r.fim); r.C = C; r.dur = dur;
  return r;
}

// ---------- último informe de avanço até a data (tabela 17)
export function ultimoAvanco(avanco, corte) {
  const u = {};
  for (const a of avanco) if (a.semana_fim <= corte && (!u[a.id_atividade] || a.semana_fim >= u[a.id_atividade].semana_fim)) u[a.id_atividade] = a;
  return u;
}

// ---------- convenções 8 e 10: velocidade e previsão das releases
export function agil(db, corte, mods = {}) {
  const C = calendario(db.calendario);
  const sprints = db.sprints.slice().sort((a, b) => a.numero - b.numero);
  const encerradas = sprints.filter((s) => s.data_fim <= corte).map((s) => s.id_sprint);
  const vel = {}; for (const x of db.sprint_itens) if (Number(x.concluido_na_sprint) === 1) vel[x.id_sprint] = (vel[x.id_sprint] || 0) + Number(x.pontos);
  const ult5 = encerradas.slice(-5); const vmed = ult5.reduce((s, k) => s + (vel[k] || 0), 0) / (ult5.length || 1);
  const concl = (b) => b.status === 'CONCLUIDO' && (!b.data_conclusao || b.data_conclusao <= corte);
  const releases = {}; const ultimaN = encerradas.length ? Number(encerradas.at(-1).slice(1)) : 0;
  ['R1', 'R2', 'R3'].forEach((rel, j) => {
    const alvo = ['R1', 'R2', 'R3'].slice(0, j + 1);
    const excl = mods.excluirItens || new Set();
    const rest = db.backlog_itens.filter((b) => !concl(b) && b.prioridade_moscow !== 'WONT' && alvo.includes(b.id_release) && !excl.has(b.id_item)).reduce((s, b) => s + Number(b.pontos), 0)
      + (mods.incluirItens || []).filter((x) => alvo.includes(x.id_release)).reduce((s, x) => s + Number(x.pontos), 0);
    let n = 0;
    if (rest) {
      if (!mods.ganho) n = ceil(rest / vmed);
      else { let feito = 0; while (feito < rest - 1e-9) { n++; feito += vmed + (n > mods.rampa ? mods.ganho : 0); } }
    }
    const sp = 'S' + String(ultimaN + n).padStart(2, '0');
    const real = db.releases.find((r) => r.id_release === rel)?.data_real;
    releases[rel] = { pontosRestantes: rest, sprints: n, sprint: sp, data: real && real <= corte ? real : (n ? C.fimSprint[sp] : (real || corte)), real: real && real <= corte ? real : null,
      planejada: db.releases.find((r) => r.id_release === rel)?.data_planejada };
  });
  const base = db.backlog_itens.filter((b) => b.origem === 'PLANO_INICIAL' && b.prioridade_moscow !== 'WONT');
  const ptsBase = base.reduce((s, b) => s + Number(b.pontos), 0); const ptsBaseConc = base.filter(concl).reduce((s, b) => s + Number(b.pontos), 0);
  const conc = db.backlog_itens.filter(concl);
  return { vel, ult5, vmed, releases, encerradas, ptsBase, ptsBaseConc, itensConcluidos: conc.length, pontosConcluidos: conc.reduce((s, b) => s + Number(b.pontos), 0) };
}

// ---------- convenção 11: previsão de término pela rede na data de corte
export function previsao(db, corte, lb = linhaDeBase(db), mods = {}) {
  const C = lb.C; const st = C.duAte(corte); const u = ultimoAvanco(db.avanco_semanal, corte); const ag = agil(db, corte, mods);
  if (mods.novas?.length || mods.durNova) {  // rede modificada pelo cenário (convenção 21)
    const dur = { ...lb.dur }; const dep = db.dependencias.slice();
    for (const n of mods.novas || []) { dur[n.id] = n.dur; n.links.forEach((l) => dep.push(l)); }
    const r = cpm(Object.keys(dur), dur, dep); lb = { ...lb, ordem: r.ordem, preds: r.preds, dur, ativ: { ...lb.ativ } };
    for (const n of mods.novas || []) lb.ativ[n.id] = { EF: 0 };
  }
  const durNova = mods.durNova || {};
  const duDe = (iso) => C.duAte(iso);
  const ES = {}, EF = {}, sit = {};
  const relDe = { A57: 'R1', A58: 'R2', A59: 'R3' };
  for (const i of lb.ordem) {
    const a = db.atividades.find((x) => x.id_atividade === i) || { tipo_atividade: 'NOVA' }; const inf = u[i]; const ps = lb.preds[i];
    const dNova = durNova[i];
    const cedo = (min) => Math.max(min, ...ps.map((l) => (l.t === 'TI' ? EF[l.p] + 1 + l.d : ES[l.p] + l.d)));
    if (a.tipo_atividade === 'MARCO_AGIL') {
      const r = ag.releases[relDe[i]];
      if (r.real) { ES[i] = lb.ativ[i].ES; EF[i] = duDe(r.real); sit[i] = 'CONCLUIDA'; }
      else { ES[i] = cedo(1); EF[i] = Math.max(ES[i], C.d2du.get(r.data) ?? duDe(r.data)); sit[i] = 'PREVISTA_PELA_RELEASE'; }
    } else if (inf && inf.situacao === 'CONCLUIDA') { ES[i] = duDe(inf.data_inicio_real); EF[i] = duDe(inf.data_termino_real); sit[i] = 'CONCLUIDA'; }
    else if (inf) {
      let rest = ceil(lb.dur[i] * (1 - Number(inf.avanco_acumulado_pct) / 100));
      if (dNova != null) rest = Math.max(1, rest - (lb.dur[i] - dNova));  // em andamento: reduz o restante na mesma quantidade
      ES[i] = duDe(inf.data_inicio_real); EF[i] = st + rest; sit[i] = 'EM_ANDAMENTO';
    }
    else { ES[i] = cedo(st + 1); EF[i] = ES[i] + (dNova != null ? dNova : lb.dur[i]) - 1; sit[i] = 'NAO_INICIADA'; }
  }
  const fim = Math.max(...Object.values(EF)); const contrato = C.d2du.get(P.contrato);
  // cadeia que define o término
  const cadeia = []; let i = Object.keys(EF).find((k) => EF[k] === fim);
  while (i) { cadeia.push(i); if (sit[i] === 'CONCLUIDA') break;
    const amarra = lb.preds[i].filter((l) => (l.t === 'TI' ? EF[l.p] + 1 + l.d : ES[l.p] + l.d) === ES[i]); i = amarra[0]?.p; }
  const ativ = {}; for (const k of lb.ordem) ativ[k] = { ES: ES[k], EF: EF[k], situacao: sit[k], inicio: C.data(ES[k]), termino: C.data(EF[k]),
    desvio: EF[k] - (lb.ativ[k]?.EF || EF[k]), avanco: u[k] ? Number(u[k].avanco_acumulado_pct) : (sit[k] === 'CONCLUIDA' ? 100 : 0), naCadeia: cadeia.includes(k) };
  return { ativ, fim, termino: C.data(fim), duAlemContrato: fim - contrato, custoAtraso: Math.max(0, fim - contrato) * P.atrasoDu,
    desvioLb: fim - lb.fim, cadeia: cadeia.reverse(), agil: ag };
}

// ---------- convenções 3 a 7: valor agregado
export function valorAgregado(db, corte, lb = linhaDeBase(db)) {
  const C = lb.C; const d = C.duAte(corte); const u = ultimoAvanco(db.avanco_semanal, corte);
  const orc = {}; db.orcamento_linha_de_base.forEach((o) => (orc[o.id_atividade] = (orc[o.id_atividade] || 0) + Number(o.valor_orcado_rs)));
  const equipe = Object.fromEntries(db.equipe.map((p) => [p.id_pessoa, Number(p.custo_hora_rs)]));
  const atvEap = Object.fromEntries(db.atividades.map((a) => [a.id_atividade, a.codigo_eap]));
  const ent = (cod) => (cod ? cod.split('.').slice(0, 2).join('.') : null);
  const porEntrega = {}; const E = (k) => (porEntrega[k] ||= { entrega: k, ont: 0, vp: 0, va: 0, cr: 0 });
  for (const [i, v] of Object.entries(orc)) {
    const a = lb.ativ[i]; const frac = Math.min(1, Math.max(0, (d - a.ES + 1) / a.dur)); const e = E(ent(atvEap[i]));
    e.ont += v; e.vp += v * frac; e.va += v * (u[i] ? Number(u[i].avanco_acumulado_pct) / 100 : 0);
  }
  // custo real: lançamentos (tab. 19) + horas (tab. 18, semanas encerradas até a data) x custo/hora
  let crAgil = 0;
  for (const c of db.custos_realizados) {
    if (c.data > corte) continue;
    if (c.frente === 'PREDITIVA') E(ent(c.codigo_eap || atvEap[c.id_atividade])).cr += Number(c.valor_rs);
    else if (c.frente === 'AGIL') crAgil += Number(c.valor_rs);
  }
  for (const h of db.apontamento_horas) {
    if (addDias(h.semana_inicio, 4) > corte || h.tipo_item === 'GESTAO') continue;
    const v = (Number(h.horas_normais) + Number(h.horas_extras) * P.fatorHE) * (equipe[h.id_pessoa] || 0);
    if (h.tipo_item === 'ATIVIDADE') E(ent(atvEap[h.id_item])).cr += v; else crAgil += v;
  }
  // frente ágil
  const ag = agil(db, corte); let vpAg = 0;
  for (const s of db.sprints) {
    if (Number(s.planejada_na_linha_de_base) !== 1) continue;
    if (s.data_fim <= corte) vpAg += Number(s.orcamento_sprint_rs);
    else if (s.data_inicio <= corte) { const dd = C.duAte(corte) - C.duAte(addDias(s.data_inicio, -1)); vpAg += Number(s.orcamento_sprint_rs) * dd / Number(s.dias_uteis); }
  }
  const agilL = { entrega: 'Frente ágil', ont: P.ontAgil, vp: vpAg, va: P.ontAgil * ag.ptsBaseConc / ag.ptsBase, cr: crAgil };
  const ind = (x) => ({ ...x, vprazo: x.va - x.vp, vcusto: x.va - x.cr, idp: x.vp ? x.va / x.vp : null, idc: x.cr ? x.va / x.cr : null });
  const soma = (arr, nome) => arr.reduce((s, x) => ({ entrega: nome, ont: s.ont + x.ont, vp: s.vp + x.vp, va: s.va + x.va, cr: s.cr + x.cr }), { ont: 0, vp: 0, va: 0, cr: 0 });
  const entregas = Object.values(porEntrega).sort((a, b) => a.entrega.localeCompare(b.entrega, 'pt', { numeric: true }));
  const pred = soma(entregas, 'Frente preditiva'); const proj = soma([pred, agilL], 'Projeto');
  const pj = ind(proj); pj.ent = pj.ont / pj.idc; pj.idpt = (pj.ont - pj.va) / (pj.ont - pj.cr);
  return { entregas: entregas.map(ind), preditiva: ind(pred), agil: ind(agilL), projeto: pj };
}

// ---------- números de controle (seção 3 do dossiê) na data de corte
export function controle(db, corte) {
  const h = db.apontamento_horas.filter((x) => addDias(x.semana_inicio, 4) <= corte || x.semana_inicio <= corte);
  const c = db.custos_realizados.filter((x) => x.data <= corte);
  const ag = agil(db, corte);
  const folha = db.cargos_salarios.reduce((s, p) => s + Number(p.remuneracao_mensal_rs) * (1 + Number(p.encargos_pct) / 100) + Number(p.beneficios_mensais_rs), 0);
  return [
    ['Horas apontadas (normais + extras), tab. 18', h.reduce((s, x) => s + Number(x.horas_normais) + Number(x.horas_extras), 0), [11708.5, 12344.0]],
    ['Linhas de apontamento de horas, tab. 18', h.length, [508, 532]],
    ['Custos lançados (R$), tab. 19', c.reduce((s, x) => s + Number(x.valor_rs), 0), [35573360.67, 35888081.96]],
    ['Custos da frente preditiva (R$), tab. 19', c.filter((x) => x.frente === 'PREDITIVA').reduce((s, x) => s + Number(x.valor_rs), 0), [34632983.98, 34869444.80]],
    ['Lançamentos de custo, tab. 19', c.length, [142, 148]],
    ['Itens no backlog, tab. 14', db.backlog_itens.filter((b) => !b.data_criacao || b.data_criacao <= corte).length, [94, 96]],
    ['Itens concluídos, tab. 14', ag.itensConcluidos, [65, 73]],
    ['Pontos concluídos, tab. 14', ag.pontosConcluidos, [209, 224]],
    ['Transições de status, tab. 21', db.itens_transicoes.filter((t) => t.data <= corte).length, [297, 329]],
    ['Informes de avanço, tab. 17', db.avanco_semanal.filter((a) => a.semana_fim <= corte).length, [259, 267]],
    ['Homens-hora das equipes, tab. 42', db.producao_semanal.filter((p) => p.semana_fim <= corte).reduce((s, p) => s + Number(p.hh_trabalhadas), 0), [15860, 17019]],
    ['Linhas de produção semanal, tab. 42', db.producao_semanal.filter((p) => p.semana_fim <= corte).length, [57, 63]],
    ['Custo mensal da folha (R$), tab. 39', folha, [282910.40, 282910.40]],
  ].map(([indicador, valor, [h30, h13]]) => ({ indicador, valor, esperado30: h30, esperado13: h13 }));
}

// ---------- convenção 12: exposição a riscos
export function riscos(db) {
  const ab = db.riscos_registro.filter((r) => r.status === 'ABERTO' && r.tipo_risco === 'AMEACA')
    .map((r) => ({ ...r, vme: Number(r.probabilidade_pct) / 100 * Number(r.impacto_custo_rs) })).sort((a, b) => b.vme - a.vme);
  const exposicao = ab.reduce((s, r) => s + r.vme, 0);
  return { abertas: ab, exposicao, cobertura: P.contingencia / exposicao };
}

// ---------- convenções 16, 21, 22 e 23: caso de negócio e cenários
export function casoNegocio(db, { varBen = 0, varOp = 0, extraAno0 = 0, mesesAtraso = 0 } = {}) {
  const anos = db.caso_de_negocio.slice().sort((a, b) => a.ano - b.ano).map((a) => ({ ano: Number(a.ano),
    inv: Number(a.investimento_rs) + (Number(a.ano) === 0 ? extraAno0 : 0),
    ben: Number(a.beneficio_bruto_rs) * (1 + varBen / 100), op: Number(a.ano) === 0 ? 0 : Number(a.custo_operacional_rs) + varOp }));
  anos.forEach((a) => (a.fluxo = a.ben - a.op - a.inv));
  const a1 = anos.find((a) => a.ano === 1); a1.perdaAtraso = a1.fluxo * mesesAtraso / 12; a1.fluxo -= a1.perdaAtraso;
  let acum = 0, payback = null;
  for (const a of anos) { const antes = acum; acum += a.fluxo; a.acumulado = acum; if (payback == null && antes < 0 && acum >= 0) payback = a.ano - 1 + (-antes / a.fluxo); }
  const vpl = anos.reduce((s, a) => s + a.fluxo / Math.pow(1 + P.tma, a.ano), 0);
  return { anos, vpl, payback };
}

export function cenario(db, ids, corte = P.status) {
  ids = [].concat(ids).filter((c) => c !== 'C1');
  const lb = linhaDeBase(db); const ev = valorAgregado(db, corte, lb); const ag0 = agil(db, corte);
  const custoPonto = ev.agil.cr / ag0.pontosConcluidos;
  const mods = { durNova: {}, novas: [], excluirItens: new Set(), incluirItens: [], ganho: 0, rampa: 0 };
  let custoAtiv = 0, pts = 0, recursos = 0, invest = 0, varBen = 0, varOp = 0, parcela = 0, gatilho = null;
  for (const id of ids) {
    const c = db.cenarios.find((x) => x.id_cenario === id);
    varBen += Number(c.variacao_beneficio_pct); varOp += Number(c.variacao_custo_operacional_anual_rs); invest += Number(c.investimento_adicional_rs);
    if (Number(c.parcela_beneficio_antecipada_pct)) { parcela = Number(c.parcela_beneficio_antecipada_pct) / 100; gatilho = c.id_atividade_gatilho; }
    for (const a of db.cenario_atividades.filter((x) => x.id_cenario === id)) {
      custoAtiv += Number(a.custo_adicional_rs);
      if (a.acao === 'ALTERAR_DURACAO') mods.durNova[a.id_atividade] = Number(a.duracao_du);
      else if (a.acao === 'EXCLUIR') mods.durNova[a.id_atividade] = 0;
      else {
        const links = [];
        const lig = (txt, comoPred) => (txt || '').split(';').filter(Boolean).forEach((t) => { const [o, tp, d] = t.split(':');
          links.push(comoPred ? { id_predecessora: o, id_sucessora: a.id_atividade, tipo_dependencia: tp, defasagem_du: Number(d) }
                              : { id_predecessora: a.id_atividade, id_sucessora: o, tipo_dependencia: tp, defasagem_du: Number(d) }); });
        lig(a.predecessoras, true); lig(a.sucessoras, false);
        mods.novas.push({ id: a.id_atividade, dur: Number(a.duracao_du), links });
      }
    }
    for (const b of db.cenario_backlog.filter((x) => x.id_cenario === id)) {
      if (b.acao === 'EXCLUIR') { if (!mods.excluirItens.has(b.id_item)) { mods.excluirItens.add(b.id_item); pts -= Number(b.pontos); } }
      else { mods.incluirItens.push(b); pts += Number(b.pontos); }
    }
    for (const r of db.cenario_recursos.filter((x) => x.id_cenario === id)) {
      recursos += Number(r.quantidade) * Number(r.custo_mensal_rs) * Number(r.meses);
      mods.ganho += Number(r.ganho_velocidade_pontos_por_sprint); mods.rampa = Math.max(mods.rampa, Number(r.sprints_de_rampa));
    }
  }
  const pv = previsao(db, corte, lb, mods);
  const ent = ev.projeto.ent + custoAtiv + pts * custoPonto + recursos + invest;
  const ontProj = ev.projeto.ont;
  const mesesTerm = diasCorridos(lb.termino, pv.termino) / 30.4;
  let meses = mesesTerm, mesesGat = null;
  if (parcela && gatilho) { mesesGat = diasCorridos(lb.termino, pv.ativ[gatilho].termino) / 30.4; meses = parcela * mesesGat + (1 - parcela) * mesesTerm; }
  const cn = casoNegocio(db, { varBen, varOp, extraAno0: ent - ontProj, mesesAtraso: meses });
  const custoAtraso = Math.max(0, pv.duAlemContrato) * P.atrasoDu;
  return { ids: ids.length ? ids : ['C1'], termino: pv.termino, duAlemContrato: pv.duAlemContrato, meses, mesesGat, ent, custoAtiv, pts, custoPonto, recursos,
    varBen, varOp, vpl: cn.vpl, payback: cn.payback, custoAtraso, resultado: cn.vpl - custoAtraso, anos: cn.anos, cadeia: pv.cadeia, releases: pv.agil.releases, previsao: pv };
}

// ---------- R7 · riscos: matriz 5x5 (faixas da folha M6) e consumo da reserva
export function faixaProb(p) { return p <= 10 ? 1 : p <= 30 ? 2 : p <= 50 ? 3 : p <= 70 ? 4 : 5; }
export function faixaImpacto(v, ont = P.ontPred + P.ontAgil) { const f = v / ont * 100; return f < 0.25 ? 1 : f < 0.5 ? 2 : f < 1 ? 3 : f <= 2 ? 4 : 5; }
export function reservas(db, corte) {
  const oc = db.riscos_ocorrencias.filter((o) => o.data <= corte);
  const cont = oc.filter((o) => o.id_risco).reduce((s, o) => s + Number(o.impacto_custo_real_rs), 0);
  const ger = oc.filter((o) => !o.id_risco).reduce((s, o) => s + Number(o.impacto_custo_real_rs), 0);
  return { ocorrencias: oc, contingenciaUsada: cont, gerencialUsada: ger, contingenciaSaldo: P.contingencia - cont, gerencialSaldo: P.gerencial - ger };
}

// ---------- R9 · contratos: previsto x pago, multa (convenção 14) e seleção de fornecedor (convenção 15)
export function contratos(db, corte) {
  return db.contratos.map((c) => {
    const m = db.contratos_medicoes.filter((x) => x.id_contrato === c.id_contrato);
    const pagas = m.filter((x) => x.data_real && x.data_real <= corte);
    const previstoAte = m.filter((x) => x.data_prevista <= corte).reduce((s, x) => s + Number(x.valor_previsto_rs), 0);
    const pago = pagas.reduce((s, x) => s + Number(x.valor_pago_rs), 0);
    const prevPagas = pagas.reduce((s, x) => s + Number(x.valor_previsto_rs), 0);
    const ultimo = m.slice().sort((a, b) => a.data_prevista.localeCompare(b.data_prevista)).at(-1);
    let atraso = 0;
    if (ultimo && ultimo.data_prevista < corte) atraso = Math.max(0, diasCorridos(ultimo.data_prevista, ultimo.data_real && ultimo.data_real <= corte ? ultimo.data_real : corte));
    const valor = Number(c.valor_contratado_rs);
    const multa = Math.min(atraso * Number(c.multa_atraso_pct_dia) / 100 * valor, Number(c.teto_multa_pct) / 100 * valor);
    const pendAtras = m.filter((x) => (!x.data_real || x.data_real > corte) && x.data_prevista < corte);
    return { ...c, fornecedor: db.fornecedores.find((f) => f.id_fornecedor === c.id_fornecedor)?.nome, medicoes: m.length, pagas: pagas.length, previstoAte, pago,
      desvioPago: pago - prevPagas, ressalvas: pagas.filter((x) => x.aceite === 'APROVADO_COM_RESSALVA').length, nc: pagas.reduce((s, x) => s + Number(x.nao_conformidades || 0), 0),
      atrasoUltimoMarco: atraso, multa, medicoesAtrasadas: pendAtras.length };
  });
}
export function selecaoFornecedor(db) {
  const pr = db.propostas_fornecedores; const min = (k) => Math.min(...pr.map((p) => Number(p[k]))); const max = (k) => Math.max(...pr.map((p) => Number(p[k])));
  const w = Object.fromEntries(db.projeto_parametros.filter((p) => p.parametro.startsWith('peso_criterio_')).map((p) => [p.parametro.slice(14), Number(p.valor)]));
  return pr.map((p) => { const n = { preco: min('preco_rs') / p.preco_rs, tecnica: p.nota_tecnica / 10, prazo: min('prazo_du') / p.prazo_du,
    experiencia: p.projetos_similares / max('projetos_similares'), garantia: p.garantia_meses / max('garantia_meses') };
    return { ...p, fornecedor: db.fornecedores.find((f) => f.id_fornecedor === p.id_fornecedor)?.nome || p.id_fornecedor, ...Object.fromEntries(Object.entries(n).map(([k, v]) => ['n_' + k, v])),
      nota: Object.entries(n).reduce((s, [k, v]) => s + (w[k] || 0) * v, 0) }; }).sort((a, b) => b.nota - a.nota);
}

// ---------- R14 · pessoas (convenções 17 a 19)
const mesDe = (iso) => iso.slice(0, 7);
export function pessoas(db, corte, terminoPrevisto) {
  const C = calendario(db.calendario); const fech = (m) => addDias(m + '-01', 40).slice(0, 7) <= corte.slice(0, 7) && m < corte.slice(0, 7);
  return db.equipe.map((p) => {
    const f = db.cargos_salarios.find((x) => x.id_pessoa === p.id_pessoa);
    const mensal = Number(f.remuneracao_mensal_rs) * (1 + Number(f.encargos_pct) / 100) + Number(f.beneficios_mensais_rs);
    const ch = Math.round(mensal / Number(f.horas_mensais));
    const hs = db.apontamento_horas.filter((h) => h.id_pessoa === p.id_pessoa && h.semana_inicio <= corte);
    const porMes = {}; hs.forEach((h) => { const m = mesDe(h.semana_inicio); porMes[m] = (porMes[m] || 0) + Number(h.horas_normais) + Number(h.horas_extras); });
    const plan = Object.fromEntries(db.alocacao_planejada.filter((a) => a.id_pessoa === p.id_pessoa).map((a) => [mesDe(a.mes), Number(a.horas_planejadas)]));
    const meses = [...new Set([...Object.keys(porMes), ...Object.keys(plan)])].sort().filter((m) => m < corte.slice(0, 7));
    const desvios = meses.map((m) => ({ mes: m, plan: plan[m] || 0, apont: porMes[m] || 0, desvio: (porMes[m] || 0) - (plan[m] || 0),
      pct: plan[m] ? ((porMes[m] || 0) - plan[m]) / plan[m] : null })).filter((x) => x.plan || x.apont);
    const fechados = meses.slice(-3); const media3 = fechados.reduce((s, m) => s + (porMes[m] || 0), 0) / (fechados.length || 1);
    const ini = f.mes_do_reajuste > addDias(corte, 31).slice(0, 7) + '-01' ? f.mes_do_reajuste : addDias(corte, 31).slice(0, 7) + '-01';
    const mesesReaj = terminoPrevisto ? Math.max(0, diasCorridos(ini, terminoPrevisto) / 30.4) : 0;
    const reajuste = media3 * mesesReaj * ch * Number(f.reajuste_previsto_pct) / 100;
    const custoHoras = hs.reduce((s, h) => s + (Number(h.horas_normais) + Number(h.horas_extras) * P.fatorHE) * Number(p.custo_hora_rs), 0);
    return { ...p, mensal, custoHoraCalc: ch, confere: ch === Number(p.custo_hora_rs), horas: hs.reduce((s, h) => s + Number(h.horas_normais) + Number(h.horas_extras), 0),
      custoHoras, desvios, mesesAcima20: desvios.filter((x) => x.pct != null && Math.abs(x.pct) > 0.2).length, reajuste, media3, mesReaj: ini.slice(0, 7) };
  });
}
export function devs(db, corte) {
  const eq = Object.fromEntries(db.equipe.map((p) => [p.id_pessoa, Number(p.custo_hora_rs)]));
  return db.equipe.filter((p) => p.frente === 'AGIL').map((p) => {
    const hs = db.apontamento_horas.filter((h) => h.id_pessoa === p.id_pessoa && h.tipo_item === 'SPRINT' && h.semana_inicio <= corte);
    const horas = hs.reduce((s, h) => s + Number(h.horas_normais) + Number(h.horas_extras), 0);
    const custo = hs.reduce((s, h) => s + (Number(h.horas_normais) + Number(h.horas_extras) * P.fatorHE) * eq[p.id_pessoa], 0);
    const pts = db.backlog_itens.filter((b) => b.id_responsavel === p.id_pessoa && b.status === 'CONCLUIDO' && (!b.data_conclusao || b.data_conclusao <= corte)).reduce((s, b) => s + Number(b.pontos), 0);
    return { id: p.id_pessoa, nome: p.nome, papel: p.papel, horas, custo, pontos: pts, ptsHora: horas ? pts / horas : null, custoPonto: pts ? custo / pts : null };
  });
}

// ---------- R15 · produtividade das equipes (convenção 20)
export function produtividade(db, corte) {
  return db.produtividade_referencia.map((r) => {
    const sem = db.producao_semanal.filter((x) => x.id_atividade === r.id_atividade && x.semana_fim <= corte).sort((a, b) => a.semana_fim.localeCompare(b.semana_fim));
    const exec = sem.reduce((s, x) => s + Number(x.quantidade_executada), 0); const hh = sem.reduce((s, x) => s + Number(x.hh_trabalhadas), 0);
    const real = hh ? exec / hh : null; const ult3 = sem.slice(-3); const ef3 = ult3.reduce((s, x) => s + Number(x.efetivo_medio), 0) / (ult3.length || 1);
    const efMed = sem.reduce((s, x) => s + Number(x.efetivo_medio), 0) / (sem.length || 1);
    const resta = Math.max(0, Number(r.quantidade_total) - exec);
    return { ...r, semanas: sem.length, executado: exec, hh, real, indProd: real != null ? real / Number(r.produtividade_planejada) : null,
      efetivoMedio: sem.length ? efMed : null, efetivo3: sem.length ? ef3 : null, indEfetivo: sem.length ? efMed / Number(r.equipe_planejada_pessoas) : null,
      restante: resta, duracaoRestante: real && resta ? ceil(resta / (real * ef3 * 8)) : (sem.length ? 0 : null),
      diagnostico: !sem.length ? 'sem produção' : (efMed / r.equipe_planejada_pessoas < 0.9 && real / r.produtividade_planejada >= 0.9 ? 'falta gente'
        : real / r.produtividade_planejada < 0.9 && efMed / r.equipe_planejada_pessoas >= 0.9 ? 'baixa produtividade'
        : real / r.produtividade_planejada < 0.9 ? 'falta gente e produtividade' : 'no ritmo') };
  });
}
