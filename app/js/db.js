// Acesso ao banco (Supabase) e utilidades de formatação.
import { createClient } from '@supabase/supabase-js';
import { SUPABASE_URL, SUPABASE_KEY } from './config.js';

export const sb = createClient(SUPABASE_URL, SUPABASE_KEY);


// Lê uma tabela inteira (paginando de 1000 em 1000, limite do Supabase)
export async function tabela(nome, { select = '*', filtro = null, ordem = null, asc = true } = {}) {
  let tudo = [];
  for (let de = 0; ; de += 1000) {
    let q = sb.from(nome).select(select).range(de, de + 999);
    if (filtro) q = filtro(q);
    if (ordem) q = q.order(ordem, { ascending: asc });
    const { data, error } = await q;
    if (error) throw new Error(`${nome}: ${error.message}`);
    tudo = tudo.concat(data);
    if (data.length < 1000) break;
  }
  return tudo;
}

// ---------- formatação (pt-BR)
const nf = (d) => new Intl.NumberFormat('pt-BR', { minimumFractionDigits: d, maximumFractionDigits: d });
export const fmt = {
  rs: (v) => v == null ? '—' : 'R$ ' + nf(0).format(v),
  rs2: (v) => v == null ? '—' : 'R$ ' + nf(2).format(v),
  mi: (v) => v == null ? '—' : 'R$ ' + nf(2).format(v / 1e6) + ' mi',
  n: (v, d = 0) => v == null ? '—' : nf(d).format(v),
  pct: (v, d = 1) => v == null ? '—' : nf(d).format(v * 100) + '%',
  i: (v) => v == null ? '—' : nf(2).format(v),
  data: (s) => s ? s.split('-').reverse().join('/') : '—',
};

export function toast(msg, ms = 3500) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.style.display = 'block';
  clearTimeout(t._h); t._h = setTimeout(() => (t.style.display = 'none'), ms);
}

// Monta uma tabela HTML a partir de linhas e definição de colunas [{campo, titulo, f (formatador), t (texto à esquerda)}]
export function htmlTabela(linhas, cols, { classeLinha = null } = {}) {
  const th = cols.map((c) => `<th class="${c.t ? 't' : ''}">${c.titulo}</th>`).join('');
  const tr = linhas.map((l) => `<tr class="${classeLinha ? classeLinha(l) : ''}">` + cols.map((c) => {
    const v = l[c.campo];
    const txt = c.f ? c.f(v, l) : (v ?? '—');
    const cls = [c.t ? 't' : '', c.cor ? c.cor(v, l) : ''].join(' ');
    return `<td class="${cls}">${txt}</td>`;
  }).join('') + '</tr>').join('');
  return `<table><thead><tr>${th}</tr></thead><tbody>${tr}</tbody></table>`;
}

export const dataCorte = () => document.getElementById('dataCorte').value;

// ---------- cache das tabelas usadas nos cálculos (recarrega depois de cada lançamento)
const TABELAS = ['projeto_parametros', 'caso_de_negocio', 'partes_interessadas', 'equipe', 'matriz_alcadas', 'eap', 'atividades', 'dependencias',
  'orcamento_linha_de_base', 'marcos', 'calendario', 'compressao_opcoes', 'epicos', 'backlog_itens', 'sprints', 'releases', 'avanco_semanal',
  'apontamento_horas', 'custos_realizados', 'sprint_itens', 'itens_transicoes', 'impedimentos', 'implantacoes', 'defeitos', 'inspecoes_aceite',
  'riscos_registro', 'riscos_ocorrencias', 'mudancas_solicitacoes', 'fornecedores', 'contratos', 'contratos_medicoes', 'propostas_fornecedores',
  'reunioes', 'engajamento_mensal', 'pulso_equipe', 'okr_medicoes', 'funil_piloto_semanal', 'elementos_3d', 'cargos_salarios',
  'alocacao_planejada', 'produtividade_referencia', 'producao_semanal', 'cenarios', 'cenario_atividades', 'cenario_backlog', 'cenario_recursos'];
let cache = null;
export async function dados(forcar = false) {
  if (cache && !forcar) return cache;
  const arr = await Promise.all(TABELAS.map((t) => tabela(t, { ordem: 'id' })));
  cache = Object.fromEntries(TABELAS.map((t, i) => [t, arr[i]]));
  return cache;
}
export const limparCache = () => { cache = null; };
