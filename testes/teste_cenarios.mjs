// Confere o simulador com a tabela de controle do dossiê (C1, C3, C4) depois dos boletins (banco de teste local).
import { execSync } from 'child_process';
import * as K from '../app/js/calc.js';
const TAB = ['projeto_parametros','caso_de_negocio','equipe','atividades','dependencias','orcamento_linha_de_base','calendario','backlog_itens','sprints','releases','avanco_semanal','apontamento_horas','custos_realizados','sprint_itens','cenarios','cenario_atividades','cenario_backlog','cenario_recursos','cargos_salarios','itens_transicoes','producao_semanal','riscos_registro','eap'];
const db = {};
for (const t of TAB) db[t] = JSON.parse(execSync(`psql -h /tmp/pgt -p 5499 -U postgres -tAc "select coalesce(json_agg(x),'[]') from (select * from ${t} order by id) x"`).toString());
const brl = (v) => v.toLocaleString('pt-BR', { maximumFractionDigits: 0 });
for (const ids of [['C1'], ['C2'], ['C3'], ['C4'], ['C5'], ['C6'], ['C2', 'C3']]) {
  const r = K.cenario(db, ids);
  console.log(ids.join('+').padEnd(6), r.termino, 'du+', r.duAlemContrato, 'meses', r.meses.toFixed(2), 'ENT', brl(r.ent), 'VPL', brl(r.vpl), 'payback', r.payback?.toFixed(2), 'resultado', brl(r.resultado), 'R2', r.releases.R2.data, 'R3', r.releases.R3.data);
}
console.log('esperado: C1 10/05/2027 1 0,43 41.764.252 · C3 10/05/2027 1 0,43 41.389.882 · C4 23/06/2027 32 1,88 42.969.789');
