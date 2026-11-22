// R7/R8 riscos e mudanças · R9/R10 contratos e partes interessadas · R14/R15 pessoas e produtividade.
import Chart from 'chart.js/auto';
import { dados, fmt, htmlTabela, dataCorte } from './db.js';
import * as K from './calc.js';

const kpi = (t, v, s = '', c = '') => `<div class="kpi ${c}"><small>${t}</small><b>${v}</b><small>${s}</small></div>`;
const T = (campo, titulo, f, o = {}) => ({ campo, titulo, f, ...o });
let gs = []; const limpar = () => { gs.forEach((g) => g.destroy()); gs = []; };

// ---------------- R7 e R8
export async function paginaRiscos(alvo) {
  limpar(); const db = await dados(); const d = dataCorte(); const rk = K.riscos(db); const rs = K.reservas(db, d);
  const mat = Array.from({ length: 5 }, () => Array(5).fill(''));
  rk.abertas.forEach((r) => { const p = K.faixaProb(Number(r.probabilidade_pct)), i = K.faixaImpacto(Number(r.impacto_custo_rs)); mat[5 - p][i - 1] += `<span class="chip crit">${r.id_risco}</span> `; });
  const cor = (p, i) => { const s = p * i; return s >= 12 ? '#f8d0d0' : s >= 6 ? '#fde9c8' : '#e3f1e3'; };
  const al = db.matriz_alcadas;
  const sm = db.mudancas_solicitacoes.filter((m) => m.data_abertura <= d).map((m) => {
    const a = al.find((x) => x.nivel_decisor === m.nivel_decisor); const dentro = !a || ((!a.limite_custo_rs || m.impacto_custo_rs <= a.limite_custo_rs) && (!a.limite_prazo_du || m.impacto_prazo_du <= a.limite_prazo_du) && (m.tipo_mudanca !== 'ESCOPO' || a.pode_alterar_escopo === 'SIM'));
    const quem = al.slice().sort((x, y) => (x.limite_custo_rs ?? 1e12) - (y.limite_custo_rs ?? 1e12)).find((x) => (!x.limite_custo_rs || m.impacto_custo_rs <= x.limite_custo_rs) && (!x.limite_prazo_du || m.impacto_prazo_du <= x.limite_prazo_du) && (m.tipo_mudanca !== 'ESCOPO' || x.pode_alterar_escopo === 'SIM'));
    return { ...m, alcadaOk: m.nivel_decisor ? dentro : null, quemDeveria: quem?.nivel_decisor };
  });
  const diretos = db.backlog_itens.filter((b) => b.origem === 'PEDIDO_DIRETO' && (!b.data_criacao || b.data_criacao <= d));
  const durante = db.sprint_itens.filter((x) => x.origem_na_sprint === 'ADICIONADO_DURANTE');
  alvo.innerHTML = `<h2>Riscos, reservas e mudanças · ${fmt.data(d)}</h2>
  <div class="kpis">${kpi('Exposição (VME das ameaças abertas)', fmt.rs(rk.exposicao), `${rk.abertas.length} ameaças abertas`)}
    ${kpi('Contingência consumida', fmt.rs(rs.contingenciaUsada), `de ${fmt.rs(K.P.contingencia)} · saldo ${fmt.rs(rs.contingenciaSaldo)}`, rs.contingenciaSaldo < 0 ? 'ruim' : '')}
    ${kpi('Saldo da contingência − exposição', fmt.rs(rs.contingenciaSaldo - rk.exposicao), 'o que falta para cobrir os riscos abertos', rs.contingenciaSaldo - rk.exposicao < 0 ? 'ruim' : 'bom')}
    ${kpi('Reserva gerencial consumida', fmt.rs(rs.gerencialUsada), `imprevistos · saldo ${fmt.rs(rs.gerencialSaldo)}`)}
    ${kpi('Pedidos diretos sem mudança', diretos.length + ' itens', diretos.reduce((s, b) => s + Number(b.pontos), 0) + ' pontos · todos da montadora (PI13)', diretos.length ? 'ruim' : '')}
    ${kpi('Itens adicionados durante sprints', durante.length, durante.reduce((s, x) => s + Number(x.pontos), 0) + ' pontos (tabela 20)')}</div>
  <div class="grade">
    <div class="cartao"><h3>Matriz probabilidade × impacto (ameaças abertas)</h3>
      <table><tr><th>P \\ I</th>${[1, 2, 3, 4, 5].map((i) => `<th>${i}</th>`).join('')}</tr>${mat.map((l, k) => `<tr><th>${5 - k}</th>${l.map((c, i) => `<td class="t" style="background:${cor(5 - k, i + 1)};height:34px">${c}</td>`).join('')}</tr>`).join('')}</table>
      <p class="fonte">Faixas da folha M6. Probabilidade: 1 até 10%; 2 até 30%; 3 até 50%; 4 até 70%; 5 acima. Impacto em % do ONT (R$ 39.009.276): 1 &lt; 0,25%; 2 &lt; 0,5%; 3 &lt; 1%; 4 até 2%; 5 acima.</p></div>
    <div class="cartao"><h3>Ocorrências (riscos materializados e imprevistos)</h3>${htmlTabela(rs.ocorrencias, [T('id_ocorrencia', 'Id', null, { t: 1 }), T('data', 'Data', fmt.data), T('id_risco', 'Risco', (v) => v || 'imprevisto', { t: 1 }),
      T('descricao', 'Descrição', null, { t: 1 }), T('impacto_custo_real_rs', 'Custo', fmt.rs), T('impacto_prazo_real_du', 'Prazo (du)'), T('id_risco', 'Reserva', (v) => (v ? 'contingência' : 'gerencial'), { t: 1 })])}
      <p class="fonte">Premissa: ocorrência de risco identificado consome a contingência; imprevisto (sem id de risco) consome a reserva gerencial.</p></div>
  </div>
  <div class="cartao" style="margin-top:12px"><h3>Ameaças abertas por valor esperado (convenção 12)</h3>${htmlTabela(rk.abertas, [T('id_risco', 'Id', null, { t: 1 }), T('descricao', 'Risco', null, { t: 1 }),
    T('categoria', 'Categoria', null, { t: 1 }), T('probabilidade_pct', 'Prob. (%)'), T('impacto_custo_rs', 'Impacto (R$)', fmt.rs), T('impacto_prazo_du', 'Prazo (du)'),
    T('vme', 'VME (R$)', fmt.rs), T('estrategia_resposta', 'Resposta', null, { t: 1 }), T('id_responsavel', 'Dono', null, { t: 1 })])}</div>
  <div class="cartao" style="margin-top:12px"><h3>Solicitações de mudança e alçadas (tabelas 28 e 05)</h3>${htmlTabela(sm, [T('id_mudanca', 'SM', null, { t: 1 }), T('data_abertura', 'Abertura', fmt.data),
    T('id_solicitante', 'Solicitante', null, { t: 1 }), T('descricao', 'Descrição', null, { t: 1 }), T('tipo_mudanca', 'Tipo', null, { t: 1 }), T('impacto_custo_rs', 'Custo', fmt.rs),
    T('impacto_prazo_du', 'du'), T('impacto_pontos', 'pt'), T('status', 'Situação', null, { t: 1 }), T('nivel_decisor', 'Decidiu', (v) => v || '—', { t: 1 }),
    T('quemDeveria', 'Alçada exigida', null, { t: 1 }), T('alcadaOk', 'Dentro da alçada?', (v) => (v == null ? '—' : v ? '<span class="ok">sim</span>' : '<span class="erro">não</span>'))])}</div>
  <div class="cartao" style="margin-top:12px"><h3>Escopo que entrou sem controle de mudança (pedidos diretos)</h3>${htmlTabela(diretos, [T('id_item', 'Item', null, { t: 1 }), T('titulo', 'Título', null, { t: 1 }),
    T('pontos', 'Pontos'), T('id_solicitante', 'Solicitante', null, { t: 1 }), T('data_criacao', 'Criado em', fmt.data), T('status', 'Situação', null, { t: 1 })])}</div>`;
}

// ---------------- R9 e R10
export async function paginaContratos(alvo) {
  limpar(); const db = await dados(); const d = dataCorte(); const ct = K.contratos(db, d); const sel = K.selecaoFornecedor(db);
  const ins = db.inspecoes_aceite.filter((i) => i.data <= d); const porF = {};
  ins.forEach((i) => { const k = i.id_fornecedor || '—'; const o = (porF[k] ||= { fornecedor: db.fornecedores.find((f) => f.id_fornecedor === k)?.nome || 'equipe própria', n: 0, nc: 0, itens: 0, reprov: 0, ressalva: 0, custo: 0 });
    o.n++; o.nc += Number(i.itens_nao_conformes); o.itens += Number(i.itens_verificados); o.reprov += i.resultado === 'REPROVADO'; o.ressalva += i.resultado === 'APROVADO_COM_RESSALVA'; o.custo += Number(i.custo_retrabalho_rs); });
  const pi = db.partes_interessadas; const ultMes = [...new Set(db.engajamento_mensal.filter((e) => e.mes <= d).map((e) => e.mes))].sort().at(-1);
  const nivel = ['DESCONHECE', 'RESISTENTE', 'NEUTRO', 'APOIA', 'LIDERA'];
  const partes = pi.map((p) => { const e = db.engajamento_mensal.find((x) => x.id_parte === p.id_parte && x.mes === ultMes) || {};
    const q = p.poder >= 4 && p.interesse >= 4 ? 'Gerenciar de perto' : p.poder >= 4 ? 'Manter satisfeito' : p.interesse >= 4 ? 'Manter informado' : 'Monitorar';
    return { ...p, atual: e.nivel_engajamento, satisfacao: e.satisfacao, gap: nivel.indexOf(p.engajamento_desejado) - nivel.indexOf(e.nivel_engajamento), quadrante: q }; });
  const reun = db.reunioes.filter((r) => r.data <= d); const pres = reun.reduce((s, r) => s + Number(r.presentes), 0) / reun.reduce((s, r) => s + Number(r.convidados), 0);
  const comite = reun.filter((r) => r.tipo_reuniao === 'COMITE_DIRETOR');
  alvo.innerHTML = `<h2>Contratos, fornecedores e partes interessadas · ${fmt.data(d)}</h2>
  <div class="kpis">${kpi('Pago acima do previsto', fmt.rs(ct.reduce((s, c) => s + c.desvioPago, 0)), 'medições pagas × valor previsto delas', 'ruim')}
    ${kpi('Multas por atraso (conv. 14)', fmt.rs(ct.reduce((s, c) => s + c.multa, 0)), ct.filter((c) => c.multa > 0).map((c) => c.id_contrato).join(', '))}
    ${kpi('Proposta vencedora (comissionamento)', sel[0].id_proposta, `${sel[0].fornecedor} · nota ${fmt.n(sel[0].nota, 3)}`, 'bom')}
    ${kpi('Presença nas reuniões', fmt.pct(pres), `${reun.length} reuniões · patrocinador em ${reun.filter((r) => Number(r.patrocinador_presente)).length}`)}
    ${kpi('Comitê diretor', comite.length + ' reuniões', `patrocinador presente em ${comite.filter((r) => Number(r.patrocinador_presente)).length}`)}
    ${kpi('Partes abaixo do desejado', partes.filter((p) => p.gap > 0).length + ' de ' + partes.length, `mês ${ultMes ? ultMes.slice(5, 7) + '/' + ultMes.slice(0, 4) : '—'}`, partes.some((p) => p.gap > 1) ? 'ruim' : '')}</div>
  <div class="cartao"><h3>Contratos (tabelas 30 e 31)</h3>${htmlTabela(ct, [T('id_contrato', 'Contrato', null, { t: 1 }), T('fornecedor', 'Fornecedor', null, { t: 1 }), T('objeto', 'Objeto', null, { t: 1 }),
    T('tipo_contrato', 'Tipo', null, { t: 1 }), T('valor_contratado_rs', 'Valor', fmt.rs), T('pagas', 'Medições pagas', (v, l) => `${v}/${l.medicoes}`), T('pago', 'Pago', fmt.rs),
    T('desvioPago', 'Pago − previsto', fmt.rs, { cor: (v) => (v > 1 ? 'neg' : '') }), T('ressalvas', 'Ressalvas'), T('atrasoUltimoMarco', 'Atraso último marco (dias)', null, { cor: (v) => (v > 0 ? 'neg' : '') }),
    T('multa', 'Multa', fmt.rs)])}<p class="fonte">Multa = dias corridos de atraso do último marco × % ao dia × valor do contrato, limitada ao teto (convenção 14).</p></div>
  <div class="grade" style="margin-top:12px">
    <div class="cartao"><h3>Seleção do fornecedor de comissionamento (convenção 15)</h3>${htmlTabela(sel, [T('id_proposta', 'Proposta', null, { t: 1 }), T('fornecedor', 'Fornecedor', null, { t: 1 }),
      T('preco_rs', 'Preço', fmt.rs), T('n_preco', 'Preço', (v) => fmt.n(v, 3)), T('n_tecnica', 'Técnica', (v) => fmt.n(v, 3)), T('n_prazo', 'Prazo', (v) => fmt.n(v, 3)),
      T('n_experiencia', 'Exper.', (v) => fmt.n(v, 3)), T('n_garantia', 'Garantia', (v) => fmt.n(v, 3)), T('nota', 'Nota', (v) => `<b>${fmt.n(v, 3)}</b>`)])}
      <p class="fonte">Pesos: preço 35%, técnica 30%, prazo 15%, experiência 10%, garantia 10% (tabela 01).</p></div>
    <div class="cartao"><h3>Qualidade por fornecedor (inspeções, tabela 25)</h3>${htmlTabela(Object.values(porF), [T('fornecedor', 'Fornecedor', null, { t: 1 }), T('n', 'Inspeções'),
      T('nc', 'Não conformes', (v, l) => `${v} (${fmt.pct(v / l.itens)})`), T('ressalva', 'Com ressalva'), T('reprov', 'Reprovadas', null, { cor: (v) => (v ? 'neg' : '') }), T('custo', 'Retrabalho', fmt.rs)])}</div>
  </div>
  <div class="cartao" style="margin-top:12px"><h3>Partes interessadas: poder × interesse e engajamento atual</h3>${htmlTabela(partes, [T('id_parte', 'Id', null, { t: 1 }), T('parte_interessada', 'Parte', null, { t: 1 }),
    T('poder', 'Poder'), T('interesse', 'Interesse'), T('quadrante', 'Estratégia', null, { t: 1 }), T('engajamento_inicial', 'Inicial', null, { t: 1 }), T('atual', 'Atual', null, { t: 1 }),
    T('engajamento_desejado', 'Desejado', null, { t: 1 }), T('satisfacao', 'Satisfação', (v) => fmt.n(v, 1)), T('gap', 'Distância do desejado', (v) => (v > 0 ? v + ' nível(is)' : 'ok'), { cor: (v) => (v > 0 ? 'neg' : 'pos') })])}
    <p class="fonte">Alto = 4 ou 5 (folha M6). Engajamento atual = último mês da tabela 34 até a data de corte.</p></div>`;
}

// ---------------- R14 e R15
export async function paginaPessoas(alvo) {
  limpar(); const db = await dados(); const d = dataCorte(); const pv = K.previsao(db, d);
  const ps = K.pessoas(db, d, pv.termino); const dv = K.devs(db, d); const pr = K.produtividade(db, d);
  const folha = ps.reduce((s, p) => s + p.mensal, 0);
  const desv = ps.flatMap((p) => p.desvios.filter((x) => x.pct != null && Math.abs(x.pct) > 0.2).map((x) => ({ ...x, pessoa: `${p.id_pessoa} ${p.nome}` })));
  alvo.innerHTML = `<h2>Pessoas, custos de pessoal e produtividade · ${fmt.data(d)}</h2>
  <div class="kpis">${kpi('Folha mensal da equipe', fmt.rs2(folha), '17 pessoas (convenção 17)')}${kpi('Custo/hora confere com a tabela 04', ps.filter((p) => p.confere).length + ' de ' + ps.length, '', ps.every((p) => p.confere) ? 'bom' : 'ruim')}
    ${kpi('Meses com desvio > 20%', desv.length, 'planejado × apontado (convenção 18)', desv.length ? 'ruim' : '')}${kpi('Impacto dos reajustes', fmt.rs(ps.reduce((s, p) => s + p.reajuste, 0)), `até o término previsto (${fmt.data(pv.termino)}) · convenção 19`)}
    ${dv.filter((x) => x.pontos).map((x) => kpi(`${x.id} · custo por ponto`, fmt.rs(x.custoPonto), `${fmt.n(x.ptsHora, 3)} pontos/hora · ${x.pontos} pontos`)).join('')}</div>
  <div class="cartao"><h3>Produtividade das equipes contratadas (convenção 20)</h3>${htmlTabela(pr, [T('id_atividade', 'Ativ.', null, { t: 1 }), T('servico', 'Serviço', null, { t: 1 }),
    T('unidade', 'Un.', null, { t: 1 }), T('quantidade_total', 'Total', (v) => fmt.n(v, 1)), T('executado', 'Executado', (v) => fmt.n(v, 1)), T('hh', 'Hh'),
    T('real', 'Prod. real (un/Hh)', (v) => (v == null ? '—' : fmt.n(v, 3))), T('produtividade_planejada', 'Planejada', (v) => fmt.n(v, 3)),
    T('indProd', 'Índice de produtividade', (v) => (v == null ? '—' : fmt.n(v, 3)), { cor: (v) => (v != null && v < 0.9 ? 'neg' : '') }),
    T('indEfetivo', 'Índice de efetivo', (v) => (v == null ? '—' : fmt.n(v, 3)), { cor: (v) => (v != null && v < 0.9 ? 'neg' : '') }),
    T('efetivo3', 'Efetivo 3 últ. sem.', (v) => (v == null ? '—' : fmt.n(v, 1))), T('duracaoRestante', 'Duração restante (du)', (v) => (v == null ? '—' : v)),
    T('diagnostico', 'Diagnóstico', null, { t: 1 })])}
    <p class="fonte">Real = quantidade ÷ Hh (tabela 42); índice de produtividade = real ÷ planejada; índice de efetivo = efetivo médio ÷ equipe planejada; duração restante = restante ÷ (real × efetivo das 3 últimas semanas × 8 h). Diagnóstico: índice abaixo de 0,9 (premissa do grupo).</p></div>
  <div class="grade" style="margin-top:12px">
    <div class="cartao"><h3>Custo de cada pessoa</h3>${htmlTabela(ps, [T('id_pessoa', 'Id', null, { t: 1 }), T('nome', 'Nome', null, { t: 1 }), T('papel', 'Papel', null, { t: 1 }),
      T('vinculo', 'Vínculo', null, { t: 1 }), T('mensal', 'Custo mensal', fmt.rs2), T('custoHoraCalc', 'R$/h', (v, l) => `${v} ${l.confere ? '✔' : '✘'}`),
      T('horas', 'Horas apontadas'), T('custoHoras', 'Custo apontado', fmt.rs), T('reajuste', 'Reajuste até o fim', fmt.rs)])}</div>
    <div class="cartao"><h3>Meses com desvio de alocação acima de 20%</h3>${desv.length ? htmlTabela(desv, [T('pessoa', 'Pessoa', null, { t: 1 }), T('mes', 'Mês', null, { t: 1 }),
      T('plan', 'Planejado (h)', (v) => fmt.n(v, 1)), T('apont', 'Apontado (h)', (v) => fmt.n(v, 1)), T('pct', 'Desvio', (v) => fmt.pct(v), { cor: (v) => (v > 0 ? 'neg' : '') })]) : '<p class="nota">Nenhum.</p>'}
      <p class="fonte">A semana pertence ao mês da sua segunda-feira (convenção 18). Na preditiva, as pessoas são compartilhadas: compara-se apontado × planejado.</p></div>
  </div>`;
}
