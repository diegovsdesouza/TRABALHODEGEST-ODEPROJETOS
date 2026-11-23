// Fotografia dos números do sistema na data de status (banco local de teste, com os boletins lançados pelas telas).
import { execSync } from 'child_process'; import fs from 'fs';
import * as K from '../app/js/calc.js';

const T = ['projeto_parametros','caso_de_negocio','partes_interessadas','equipe','matriz_alcadas','eap','atividades','dependencias','orcamento_linha_de_base','marcos','calendario','compressao_opcoes','epicos','backlog_itens','sprints','releases','avanco_semanal','apontamento_horas','custos_realizados','sprint_itens','itens_transicoes','impedimentos','implantacoes','defeitos','inspecoes_aceite','riscos_registro','riscos_ocorrencias','mudancas_solicitacoes','fornecedores','contratos','contratos_medicoes','propostas_fornecedores','reunioes','engajamento_mensal','pulso_equipe','okr_medicoes','funil_piloto_semanal','elementos_3d','cargos_salarios','alocacao_planejada','produtividade_referencia','producao_semanal','cenarios','cenario_atividades','cenario_backlog','cenario_recursos'];
const db = {}; for (const t of T) db[t] = JSON.parse(execSync(`psql -h /tmp/pgt -p 5499 -U postgres -tAc "select coalesce(json_agg(_r),'[]') from (select * from ${t} order by id) _r"`, { maxBuffer: 1e8 }).toString());
const d = '2026-11-13'; const lb = K.linhaDeBase(db); const pv = K.previsao(db, d, lb); const ev = K.valorAgregado(db, d, lb);
const meses = []; for (const m of ['2026-02-28','2026-03-31','2026-04-30','2026-05-31','2026-06-30','2026-07-31','2026-08-31','2026-09-30','2026-10-31','2026-11-30','2026-12-31','2027-01-31','2027-02-28','2027-03-31','2027-04-30','2027-05-31']) { const e = K.valorAgregado(db, m, lb).projeto; meses.push({ mes: m, vp: e.vp, va: m <= d ? e.va : null, cr: m <= d ? e.cr : null }); }
const C = K.calendario(db.calendario);
const cen = db.cenarios.map((c) => { const r = K.cenario(db, [c.id_cenario], d); return { id: c.id_cenario, nome: c.nome_cenario, combinavel: c.combinavel_com, ...r, anos: r.anos, previsao: undefined }; });
const combos = []; for (const a of db.cenarios) for (const b of (a.combinavel_com || '').split(';').filter(Boolean)) if (a.id_cenario < b && a.id_cenario !== 'C1') { const r = K.cenario(db, [a.id_cenario, b], d); combos.push({ ids: [a.id_cenario, b], termino: r.termino, du: r.duAlemContrato, ent: r.ent, vpl: r.vpl, resultado: r.resultado, payback: r.payback }); }
const snap = { d, lb: { termino: lb.termino, fim: lb.fim, ativ: lb.ativ, dur: lb.dur }, pv: { termino: pv.termino, fim: pv.fim, du: pv.duAlemContrato, custoAtraso: pv.custoAtraso, cadeia: pv.cadeia, ativ: pv.ativ, agil: pv.agil },
  ev, meses, riscos: K.riscos(db), reservas: K.reservas(db, d), contratos: K.contratos(db, d), selecao: K.selecaoFornecedor(db), pessoas: K.pessoas(db, d, pv.termino), devs: K.devs(db, d),
  prod: K.produtividade(db, d), cen, combos, controle: K.controle(db, d), bd13: K.burndown(db, C, 'S13'), bd14: K.burndown(db, C, 'S14'), fl13: K.fluxo(db, C, 'S13'), fl14: K.fluxo(db, C, 'S14') };
fs.writeFileSync('/tmp/snap.json', JSON.stringify(snap));
console.log('ok', pv.termino, Math.round(ev.projeto.ent), combos.map((c) => c.ids.join('+') + ' ' + Math.round(c.resultado)).join(' | '));
