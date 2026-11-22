// R3 · Telas de lançamento dos boletins B1 a B10 (quinzena de campo) e do boletim surpresa.
// Cada tela é uma configuração (tabela + campos); um único motor monta o formulário, valida e grava.
// Toda linha gravada pelas telas leva fonte_registro = 'TELA' e o e-mail de quem lançou (Supabase Auth).
import { sb, dados, limparCache, fmt, toast, htmlTabela } from './db.js';

let db = null;
const SN = [['1', 'sim'], ['0', 'não']];
const opts = {
  atividades: () => db.atividades.map((a) => [a.id_atividade, `${a.id_atividade} · ${a.nome_atividade}`]),
  pessoas: () => db.equipe.map((p) => [p.id_pessoa, `${p.id_pessoa} · ${p.nome} (${p.papel})`]),
  dev: () => db.equipe.filter((p) => p.frente === 'AGIL').map((p) => [p.id_pessoa, `${p.id_pessoa} · ${p.nome}`]),
  contratos: () => db.contratos.map((c) => [c.id_contrato, `${c.id_contrato} · ${c.objeto}`]),
  fornecedores: () => db.fornecedores.map((f) => [f.id_fornecedor, `${f.id_fornecedor} · ${f.nome}`]),
  partes: () => db.partes_interessadas.map((p) => [p.id_parte, `${p.id_parte} · ${p.parte_interessada}`]),
  sprints: () => db.sprints.map((s) => [s.id_sprint, `${s.id_sprint} · ${fmt.data(s.data_inicio)} a ${fmt.data(s.data_fim)}`]),
  itens: () => db.backlog_itens.slice().sort((a, b) => a.id_item.localeCompare(b.id_item)).map((b) => [b.id_item, `${b.id_item} · ${b.titulo.slice(0, 60)}`]),
  epicos: () => db.epicos.map((e) => [e.id_epico, `${e.id_epico} · ${e.nome_epico}`]),
  riscos: () => db.riscos_registro.map((r) => [r.id_risco, `${r.id_risco} · ${r.descricao}`]),
  medicoesPendentes: () => db.contratos_medicoes.filter((m) => !m.data_real).map((m) => [m.id_medicao, `${m.id_medicao} · ${m.descricao_marco.slice(0, 50)} · prev. ${fmt.data(m.data_prevista)}`]),
  krs: () => [...new Map(db.okr_medicoes.map((o) => [o.id_resultado_chave, `${o.id_resultado_chave} · ${o.resultado_chave}`]))],
};
const proximo = (tab, campo, prefixo, dig) => {
  const n = Math.max(0, ...db[tab].map((r) => r[campo]).filter((v) => v && v.startsWith(prefixo)).map((v) => parseInt(v.slice(prefixo.length), 10) || 0));
  return prefixo + String(n + 1).padStart(dig, '0');
};
const atv = (id) => db.atividades.find((a) => a.id_atividade === id) || {};

// [campo, rótulo, tipo (data|int|num|txt|sel), {op, vazio, padrao, manter}]
const TELAS = {
  avanco: { bol: 'B1', titulo: 'Avanço semanal (preditiva)', tabela: 'avanco_semanal', ajuda: 'Um informe por atividade e semana. O avanço é acumulado (0 a 100%).',
    campos: [['semana_fim', 'Semana até (sexta)', 'data', { manter: 1 }], ['id_atividade', 'Atividade', 'sel', { op: 'atividades' }], ['avanco_acumulado_pct', 'Avanço acumulado (%)', 'int'],
      ['situacao', 'Situação', 'sel', { op: [['EM_ANDAMENTO', 'Em andamento'], ['CONCLUIDA', 'Concluída']] }], ['data_inicio_real', 'Início real', 'data'], ['data_termino_real', 'Término real', 'data', { vazio: 1 }]],
    completar: (r) => ({ ...r, id_responsavel: atv(r.id_atividade).id_responsavel }),
    validar: (r) => (r.situacao === 'CONCLUIDA') !== (r.avanco_acumulado_pct === 100) ? 'Concluída deve ter 100% (e 100% deve estar concluída).' : (r.situacao === 'CONCLUIDA' && !r.data_termino_real ? 'Atividade concluída precisa do término real.' : null) },
  horas: { bol: 'B2', titulo: 'Folha de horas', tabela: 'apontamento_horas', ajuda: 'Item: código da atividade (A12), da sprint (S14) ou GESTAO.',
    campos: [['semana_inicio', 'Semana de (segunda)', 'data', { manter: 1 }], ['id_pessoa', 'Pessoa', 'sel', { op: 'pessoas' }],
      ['tipo_item', 'Tipo', 'sel', { op: ['ATIVIDADE', 'SPRINT', 'GESTAO'] }], ['id_item', 'Item (A12, S14 ou GESTAO)', 'txt'], ['horas_normais', 'Horas normais', 'num'], ['horas_extras', 'Horas extras', 'num', { padrao: 0 }]],
    validar: (r) => r.horas_normais > 40 ? 'Mais de 40 horas normais na semana: confira a casa decimal.' : null },
  custos: { bol: 'B3', titulo: 'Custos pagos', tabela: 'custos_realizados', auto: ['id_lancamento', 'L', 5], ajuda: 'Atividade vazia só para GESTAO ou AGIL. O código da EAP vem da atividade.',
    campos: [['data', 'Data', 'data', { manter: 1 }], ['frente', 'Frente', 'sel', { op: ['PREDITIVA', 'AGIL', 'GESTAO'] }],
      ['categoria_custo', 'Categoria', 'sel', { op: ['SERVICO_CONTRATADO', 'MATERIAL', 'EQUIPAMENTO', 'LICENCAS_E_NUVEM', 'INDIRETO', 'OUTROS'] }],
      ['id_atividade', 'Atividade', 'sel', { op: 'atividades', vazio: 1 }], ['id_contrato', 'Contrato', 'sel', { op: 'contratos', vazio: 1 }], ['id_fornecedor', 'Fornecedor', 'sel', { op: 'fornecedores', vazio: 1 }],
      ['documento', 'Documento', 'txt'], ['descricao', 'Histórico', 'txt'], ['valor_rs', 'Valor (R$)', 'num']],
    completar: (r) => ({ ...r, codigo_eap: r.id_atividade ? atv(r.id_atividade).codigo_eap : null }),
    validar: (r) => r.frente === 'PREDITIVA' && !r.id_atividade ? 'Custo da preditiva sem atividade fica sem apropriação.' : null },
  medicoes: { bol: 'B3', titulo: 'Medições aceitas', tabela: 'contratos_medicoes', chave: 'id_medicao',
    ajuda: () => 'Se a medição já está prevista na tabela 31, basta o código e o pagamento (os campos vazios não apagam o que já existe). Se é nova, preencha também contrato, atividade e descrição. Previstas em aberto: ' + (opts.medicoesPendentes().map(([k]) => k).join(', ') || 'nenhuma') + '.',
    campos: [['id_medicao', 'Medição (MED-CTnn-nn)', 'txt'], ['id_contrato', 'Contrato', 'sel', { op: 'contratos', vazio: 1 }], ['id_atividade', 'Atividade', 'sel', { op: 'atividades', vazio: 1 }],
      ['descricao_marco', 'Descrição', 'txt', { vazio: 1 }], ['data_prevista', 'Data prevista', 'data', { vazio: 1 }], ['valor_previsto_rs', 'Valor previsto (R$)', 'num', { vazio: 1 }],
      ['data_real', 'Data real', 'data'], ['valor_pago_rs', 'Valor pago (R$)', 'num'],
      ['aceite', 'Aceite', 'sel', { op: ['APROVADO', 'APROVADO_COM_RESSALVA', 'PENDENTE'] }], ['nao_conformidades', 'Não conformidades', 'int', { padrao: 0 }]] },
  inspecoes: { bol: 'B4', titulo: 'Inspeções e testes de aceite', tabela: 'inspecoes_aceite', auto: ['id_inspecao', 'IN-', 3],
    campos: [['data', 'Data', 'data'], ['id_atividade', 'Atividade', 'sel', { op: 'atividades' }], ['tipo_inspecao', 'Tipo', 'sel', { op: ['LISTA_DE_VERIFICACAO', 'FAT', 'AUDITORIA_DOCUMENTAL'] }],
      ['itens_verificados', 'Itens verificados', 'int'], ['itens_nao_conformes', 'Não conformes', 'int', { padrao: 0 }], ['resultado', 'Resultado', 'sel', { op: ['APROVADO', 'APROVADO_COM_RESSALVA', 'REPROVADO'] }],
      ['id_fornecedor', 'Fornecedor', 'sel', { op: 'fornecedores', vazio: 1 }], ['horas_retrabalho', 'Retrabalho (h)', 'num', { padrao: 0 }], ['custo_retrabalho_rs', 'Custo do retrabalho (R$)', 'num', { padrao: 0 }]] },
  sprint: { bol: 'B5', titulo: 'Planejamento da sprint', tabela: 'sprints', chave: 'id_sprint', ajuda: 'Atualiza a capacidade e a meta da sprint.',
    campos: [['id_sprint', 'Sprint', 'sel', { op: 'sprints' }], ['pessoas_dia_disponiveis', 'Pessoas-dia disponíveis', 'num'], ['horas_extras_autorizadas', 'Horas extras autorizadas', 'sel', { op: ['NAO', 'SIM'] }], ['meta_da_sprint', 'Meta', 'txt']] },
  itemSprint: { bol: 'B5', titulo: 'Itens da sprint', tabela: 'sprint_itens', ajuda: 'Um item por linha. Os pontos vêm do backlog.',
    campos: [['id_sprint', 'Sprint', 'sel', { op: 'sprints', manter: 1 }], ['id_item', 'Item', 'sel', { op: 'itens' }], ['origem_na_sprint', 'Entrada na sprint', 'sel', { op: ['PLANEJAMENTO', 'TRANSBORDO', 'ADICIONADO_DURANTE'] }]],
    completar: (r) => ({ ...r, pontos: db.backlog_itens.find((b) => b.id_item === r.id_item)?.pontos, concluido_na_sprint: 0 }),
    depois: async (r) => sb.from('backlog_itens').update({ id_sprint_atual: r.id_sprint }).eq('id_item', r.id_item) },
  backlog: { bol: 'B5', titulo: 'Novo item no backlog', tabela: 'backlog_itens', ajuda: 'Itens criados durante a quinzena (inclusive BUG de defeito).',
    campos: [['id_item', 'Item (PA-nnn)', 'txt'], ['data_criacao', 'Criado em', 'data'], ['tipo_item', 'Tipo', 'sel', { op: ['HISTORIA', 'BUG', 'TECNICA', 'SPIKE'] }], ['id_epico', 'Épico', 'sel', { op: 'epicos' }],
      ['titulo', 'Título', 'txt'], ['pontos', 'Pontos', 'int'], ['prioridade_moscow', 'Prioridade', 'sel', { op: ['MUST', 'SHOULD', 'COULD', 'WONT'] }], ['id_release', 'Release', 'sel', { op: ['R1', 'R2', 'R3'] }],
      ['origem', 'Origem', 'sel', { op: ['PEDIDO_DIRETO', 'DEFEITO', 'MUDANCA_APROVADA', 'PLANO_INICIAL'] }], ['id_solicitante', 'Solicitante', 'sel', { op: 'partes', vazio: 1 }]],
    completar: (r) => ({ ...r, status: 'A_FAZER', ordem_no_backlog: db.backlog_itens.length + 1 }),
    validar: (r) => r.origem === 'PEDIDO_DIRETO' ? 'Atenção: PEDIDO_DIRETO é escopo entrando sem solicitação de mudança. Registre mesmo assim (é o que aconteceu) e trate no diagnóstico.' : null },
  defeitos: { bol: 'B5', titulo: 'Defeitos', tabela: 'defeitos',
    campos: [['id_defeito', 'Defeito (DF-nnn)', 'txt'], ['id_item_defeito', 'Item BUG', 'sel', { op: 'itens' }], ['id_item_origem', 'Item de origem', 'sel', { op: 'itens' }],
      ['severidade', 'Severidade', 'sel', { op: ['BAIXA', 'MEDIA', 'ALTA'] }], ['ambiente_detectado', 'Ambiente', 'sel', { op: ['TESTE', 'HOMOLOGACAO', 'PRODUCAO'] }], ['data_abertura', 'Abertura', 'data'], ['data_resolucao', 'Resolução', 'data', { vazio: 1 }]] },
  quadro: { bol: 'B6', titulo: 'Quadro da sprint (mover cartões)', especial: telaQuadro },
  impedimentos: { bol: 'B7', titulo: 'Impedimentos', tabela: 'impedimentos', chave: 'id_impedimento', ajuda: 'Para fechar um impedimento existente, use o mesmo código e preencha o fechamento.',
    campos: [['id_impedimento', 'Impedimento (IP-nnn)', 'txt'], ['id_item', 'Item', 'sel', { op: 'itens' }], ['data_abertura', 'Abertura', 'data'], ['data_fechamento', 'Fechamento', 'data', { vazio: 1 }],
      ['tipo_impedimento', 'Tipo', 'sel', { op: ['DEFINICAO_PENDENTE', 'DEPENDENCIA_EXTERNA', 'AGUARDANDO_OUTRO_TIME'] }], ['dias_uteis_bloqueado', 'Dias úteis bloqueado', 'int', { vazio: 1 }], ['id_pessoa', 'Registrado por', 'sel', { op: 'dev' }]] },
  implantacoes: { bol: 'B7', titulo: 'Implantações', tabela: 'implantacoes',
    campos: [['id_implantacao', 'Implantação (IMP-nnn)', 'txt'], ['data', 'Data', 'data'], ['id_sprint', 'Sprint', 'sel', { op: 'sprints', manter: 1 }], ['ambiente', 'Ambiente', 'sel', { op: ['HOMOLOGACAO', 'PRODUCAO'] }],
      ['versao', 'Versão', 'txt'], ['itens_implantados', 'Itens', 'int'], ['tempo_ate_producao_h', 'Tempo até a publicação (h)', 'num'], ['falhou', 'Falhou', 'sel', { op: [['0', 'não'], ['1', 'sim']] }], ['tempo_restauracao_h', 'Restauração (h)', 'num', { vazio: 1 }]] },
  mudancas: { bol: 'B8', titulo: 'Solicitações de mudança', tabela: 'mudancas_solicitacoes', chave: 'id_mudanca', ajuda: 'Para decidir uma solicitação existente, use o mesmo código (ex.: SM-013).',
    campos: [['id_mudanca', 'Mudança (SM-nnn)', 'txt'], ['data_abertura', 'Abertura', 'data'], ['id_solicitante', 'Solicitante', 'sel', { op: 'partes' }], ['descricao', 'Descrição', 'txt'],
      ['tipo_mudanca', 'Tipo', 'sel', { op: ['ESCOPO', 'PRAZO', 'TECNICA'] }], ['frente', 'Frente', 'sel', { op: ['PREDITIVA', 'AGIL'] }], ['id_atividade', 'Atividade', 'sel', { op: 'atividades', vazio: 1 }],
      ['impacto_custo_rs', 'Custo (R$)', 'num'], ['impacto_prazo_du', 'Prazo (du)', 'int', { padrao: 0 }], ['impacto_pontos', 'Pontos', 'int', { padrao: 0 }],
      ['status', 'Situação', 'sel', { op: ['EM_ANALISE', 'APROVADA', 'REJEITADA'] }], ['data_decisao', 'Decisão em', 'data', { vazio: 1 }], ['nivel_decisor', 'Quem decidiu', 'sel', { op: ['GERENTE', 'PATROCINADOR', 'COMITE'], vazio: 1 }]],
    validar: (r) => { const al = db.matriz_alcadas.find((m) => m.nivel_decisor === r.nivel_decisor);
      return al && al.limite_custo_rs && r.status === 'APROVADA' && r.impacto_custo_rs > al.limite_custo_rs ? `Acima da alçada do ${r.nivel_decisor} (R$ ${fmt.n(al.limite_custo_rs)}).` : null; } },
  ocorrencias: { bol: 'B8', titulo: 'Ocorrências de risco', tabela: 'riscos_ocorrencias', auto: ['id_ocorrencia', 'OC-', 3], ajuda: 'Na quinzena de campo não houve ocorrência; use no boletim surpresa.',
    campos: [['data', 'Data', 'data'], ['id_risco', 'Risco (vazio = imprevisto)', 'sel', { op: 'riscos', vazio: 1 }], ['descricao', 'Descrição', 'txt'], ['frente', 'Frente', 'sel', { op: ['PREDITIVA', 'AGIL'] }],
      ['id_atividade', 'Atividade', 'sel', { op: 'atividades', vazio: 1 }], ['impacto_custo_real_rs', 'Custo (R$)', 'num'], ['impacto_prazo_real_du', 'Prazo (du)', 'int'], ['custo_ja_incluido_em_pagamentos', 'Custo já pago?', 'sel', { op: ['NAO', 'SIM'] }]] },
  reunioes: { bol: 'B9', titulo: 'Reuniões', tabela: 'reunioes',
    campos: [['id_reuniao', 'Reunião (RE-nnn)', 'txt'], ['data', 'Data', 'data'], ['tipo_reuniao', 'Tipo', 'sel', { op: ['STATUS_SEMANAL', 'COMITE_DIRETOR', 'PLANEJAMENTO_DA_SPRINT', 'REVISAO_DA_SPRINT', 'RETROSPECTIVA'] }],
      ['duracao_min', 'Duração (min)', 'int'], ['convidados', 'Convidados', 'int'], ['presentes', 'Presentes', 'int'], ['patrocinador_presente', 'Patrocinador presente', 'sel', { op: [['0', 'não'], ['1', 'sim']] }],
      ['decisoes_tomadas', 'Decisões', 'int'], ['pendencias_abertas', 'Pendências', 'int'], ['ata_publicada', 'Ata publicada', 'sel', { op: SN }]] },
  engajamento: { bol: 'B9', titulo: 'Engajamento das partes (mês)', tabela: 'engajamento_mensal',
    campos: [['mes', 'Mês (dia 1)', 'data', { padrao: '2026-11-01', manter: 1 }], ['id_parte', 'Parte interessada', 'sel', { op: 'partes' }], ['nivel_engajamento', 'Nível', 'sel', { op: ['DESCONHECE', 'RESISTENTE', 'NEUTRO', 'APOIA', 'LIDERA'] }],
      ['satisfacao', 'Satisfação (0 a 10)', 'num'], ['interacoes_no_mes', 'Interações', 'int']] },
  pulso: { bol: 'B9', titulo: 'Pulso da equipe', tabela: 'pulso_equipe', campos: [['id_sprint', 'Sprint', 'sel', { op: 'sprints' }], ['satisfacao_media', 'Satisfação média', 'num'], ['respostas', 'Respostas', 'int']] },
  okr: { bol: 'B9', titulo: 'Resultados-chave (OKR)', tabela: 'okr_medicoes', ajuda: 'O boletim traz duas medições por KR: registramos a 1ª em 31/10 e a 2ª em 13/11 (premissa).',
    campos: [['id_resultado_chave', 'Resultado-chave', 'sel', { op: 'krs' }], ['data_medicao', 'Data da medição', 'data', { manter: 1 }], ['valor', 'Valor', 'num']],
    completar: (r) => { const b = db.okr_medicoes.find((o) => o.id_resultado_chave === r.id_resultado_chave);
      return { ...r, id_objetivo: b.id_objetivo, objetivo: b.objetivo, resultado_chave: b.resultado_chave, unidade: b.unidade, valor_base: b.valor_base, meta: b.meta, sentido: b.sentido }; } },
  producao: { bol: 'B10', titulo: 'Produção semanal das equipes', tabela: 'producao_semanal',
    campos: [['semana_fim', 'Semana até', 'data', { manter: 1 }], ['id_atividade', 'Atividade', 'sel', { op: 'atividades' }], ['quantidade_executada', 'Quantidade executada', 'num'], ['hh_trabalhadas', 'Hh trabalhadas', 'num'], ['efetivo_medio', 'Efetivo médio', 'num']] },
  funil: { bol: 'B10', titulo: 'Funil do piloto', tabela: 'funil_piloto_semanal',
    campos: [['semana_inicio', 'Semana de', 'data'], ['alcance', 'Alcance', 'int'], ['cadastros', 'Cadastros', 'int'], ['ativados', 'Ativados', 'int'], ['ativos_na_semana', 'Ativos na semana', 'int'],
      ['retidos_4_semanas', 'Retidos 4 semanas', 'int'], ['receita_rs', 'Receita (R$)', 'num', { padrao: 0 }], ['indicacoes', 'Indicações', 'int', { padrao: 0 }], ['nps', 'NPS', 'int'], ['chamados_suporte', 'Chamados', 'int']] },
};

export async function paginaLancamentos(alvo, { usuario }) {
  db = await dados();
  const ids = Object.keys(TELAS); ids.forEach((k) => (TELAS[k].k = k));
  alvo.innerHTML = `<h2>Lançamentos · quinzena de campo (03 a 13/11) e boletim surpresa</h2>
    ${usuario ? '' : '<div class="alerta">Você está como visitante. Toque em <b>Entrar</b> para lançar. Cada integrante usa a própria conta: o sistema grava quem lançou.</div>'}
    <div class="abas">${ids.map((k) => `<button data-t="${k}"><span class="chip">${TELAS[k].bol}</span> ${TELAS[k].titulo}</button>`).join('')}</div><div id="tela"></div>`;
  const abrir = (k) => {
    sessionStorage.setItem('telaAtual', k);
    alvo.querySelectorAll('.abas button').forEach((b) => b.classList.toggle('ativo', b.dataset.t === k));
    const box = alvo.querySelector('#tela'); const t = TELAS[k];
    return t.especial ? t.especial(box, usuario) : telaGenerica(box, t, usuario);
  };
  alvo.querySelectorAll('.abas button').forEach((b) => (b.onclick = () => abrir(b.dataset.t)));
  abrir(TELAS[sessionStorage.getItem('telaAtual')] ? sessionStorage.getItem('telaAtual') : 'avanco');
}

function campoHTML([nome, rotulo, tipo, o = {}], valor) {
  const v = valor ?? o.padrao ?? '';
  if (tipo === 'sel') {
    const lista = typeof o.op === 'string' ? opts[o.op]() : o.op.map((x) => (Array.isArray(x) ? x : [x, x]));
    return `<label>${rotulo}<select name="${nome}">${o.vazio ? '<option value="">— vazio —</option>' : ''}${lista.map(([k, l]) => `<option value="${k}" ${String(k) === String(v) ? 'selected' : ''}>${l}</option>`).join('')}</select></label>`;
  }
  const it = { data: 'date', int: 'number', num: 'number', txt: 'text' }[tipo];
  return `<label>${rotulo}<input name="${nome}" type="${it}" step="${tipo === 'int' ? '1' : 'any'}" value="${v}" ${o.vazio ? '' : 'required'}></label>`;
}

function lerForm(form, t) {
  const r = {};
  for (const [nome, , tipo, o = {}] of t.campos) {
    const v = form.elements[nome].value;
    const ehNum = tipo === 'int' || tipo === 'num' || (tipo === 'sel' && Array.isArray(o.op) && Array.isArray(o.op[0]) && /^\d$/.test(o.op[0][0]));
    r[nome] = v === '' ? null : ehNum ? Number(v) : v;
  }
  if (t.auto) { const [campo, pre, dig] = t.auto; r[campo] = proximo(t.tabela, campo, pre, dig); }
  return t.completar ? t.completar(r) : r;
}

// grava: atualiza se a chave já existe; senão insere
async function gravar(tab, r, chave) {
  if (chave) {
    const { data } = await sb.from(tab).select('id').eq(chave, r[chave]).maybeSingle();
    if (data) return sb.from(tab).update(Object.fromEntries(Object.entries(r).filter(([, v]) => v !== null))).eq('id', data.id);
  }
  return sb.from(tab).insert(r);
}

function telaGenerica(box, t, usuario, valores = {}) {
  box.innerHTML = `<div class="cartao"><h3><span class="chip">${t.bol}</span> ${t.titulo}</h3><p class="nota">${typeof t.ajuda === 'function' ? t.ajuda() : (t.ajuda || '')}</p>
    <form class="lanc" data-tela="${t.k}">${t.campos.map((c) => campoHTML(c, valores[c[0]])).join('')}
      <div class="linha"><button ${usuario ? '' : 'disabled'}>Salvar</button></div></form></div>
    <div class="cartao" style="margin-top:12px"><h3>Últimos lançamentos feitos pelas telas (${t.tabela})</h3><div id="recentes">…</div></div>`;
  const form = box.querySelector('form');
  form.onsubmit = async (ev) => {
    ev.preventDefault(); const r = lerForm(form, t);
    const aviso = t.validar && t.validar(r); if (aviso && !confirm(aviso + '\n\nSalvar mesmo assim?')) return;
    const { error } = await gravar(t.tabela, r, t.chave); if (error) return toast('Erro: ' + error.message, 6000);
    if (t.depois) await t.depois(r);
    limparCache(); db = await dados();
    const manter = {}; t.campos.filter((c) => c[3]?.manter).forEach((c) => (manter[c[0]] = r[c[0]]));
    if (sessionStorage.getItem('telaAtual') === t.k) telaGenerica(box, t, usuario, manter);
    toast('Salvo em ' + t.tabela);
  };
  recentes(box.querySelector('#recentes'), t.tabela, t.campos.map((c) => c[0]).concat(t.auto ? [t.auto[0]] : []), usuario);
}

async function recentes(div, tab, campos, usuario) {
  const { data, error } = await sb.from(tab).select('*').eq('fonte_registro', 'TELA').order('lancado_em', { ascending: false }).limit(20);
  if (error) { div.textContent = error.message; return; }
  if (!data.length) { div.innerHTML = '<p class="nota">Nenhum lançamento pelas telas ainda.</p>'; return; }
  const cols = [...new Set(campos)].map((c) => ({ campo: c, titulo: c, t: 1 })).concat([{ campo: 'lancado_por_email', titulo: 'lançado por', t: 1 }]);
  if (usuario) cols.push({ campo: 'id', titulo: '', f: (v) => `<button class="perigo" data-del="${v}">apagar</button>` });
  div.innerHTML = htmlTabela(data, cols);
  div.querySelectorAll('[data-del]').forEach((b) => (b.onclick = async () => {
    if (!confirm('Apagar este lançamento?')) return;
    const { error: e } = await sb.from(tab).delete().eq('id', b.dataset.del); if (e) return toast(e.message);
    limparCache(); b.closest('tr').remove();
  }));
}

// ---------- B6 · quadro da sprint: cada movimento grava a transição (tab. 21) e atualiza o item (tab. 14 e 20)
const COLUNAS = ['A_FAZER', 'EM_ANDAMENTO', 'EM_REVISAO', 'EM_TESTE', 'CONCLUIDO'];
async function telaQuadro(box, usuario) {
  const sprintAtual = sessionStorage.getItem('sprintQuadro') || 'S14';
  const desenhar = () => {
    const sp = box.querySelector('#spQ').value; sessionStorage.setItem('sprintQuadro', sp);
    const itens = db.sprint_itens.filter((x) => x.id_sprint === sp).map((x) => ({ ...x, b: db.backlog_itens.find((b) => b.id_item === x.id_item) || {} }));
    box.querySelector('#colunas').innerHTML = COLUNAS.map((c) => `<div class="coluna"><h4>${c.replace(/_/g, ' ')}</h4>` + itens.filter((x) => (x.b.status || 'A_FAZER') === c).map((x) => `
      <div class="cartaoItem" data-i="${x.id_item}"><b>${x.id_item}</b> · ${x.pontos} pt<br>${(x.b.titulo || '').slice(0, 55)}
      <select class="para">${COLUNAS.map((d) => `<option ${d === c ? 'selected' : ''}>${d}</option>`).join('')}</select></div>`).join('') + '</div>').join('');
    box.querySelectorAll('.cartaoItem select.para').forEach((s) => (s.onchange = () => mover(s.closest('.cartaoItem').dataset.i, s.value, sp)));
  };
  const mover = async (id, para, sp) => {
    if (!usuario) return toast('Entre para mover cartões.');
    const f = box.querySelector('#movForm'); const b = db.backlog_itens.find((x) => x.id_item === id); const de = b.status || 'A_FAZER';
    if (de === para) return;
    const data = f.data.value, pessoa = f.pessoa.value; const rev = para === 'EM_REVISAO' ? Number(f.rev.value) : null;
    const t = { id_transicao: proximo('itens_transicoes', 'id_transicao', 'T', 5), id_item: id, data, status_origem: de, status_destino: para, id_pessoa: pessoa };
    const { error } = await sb.from('itens_transicoes').insert(t); if (error) return toast('Erro: ' + error.message, 6000);
    const upd = { status: para, id_sprint_atual: sp };
    if (para === 'EM_ANDAMENTO' && !b.data_inicio) upd.data_inicio = data;
    if (para === 'CONCLUIDO') upd.data_conclusao = data; else upd.data_conclusao = null;
    if (rev !== null) upd.revisao_por_par = rev;
    if (!b.id_responsavel && ['P15', 'P16'].includes(pessoa)) upd.id_responsavel = pessoa;
    await sb.from('backlog_itens').update(upd).eq('id_item', id);
    await sb.from('sprint_itens').update({ concluido_na_sprint: para === 'CONCLUIDO' ? 1 : 0 }).eq('id_sprint', sp).eq('id_item', id);
    toast(`${id}: ${de} → ${para}`); limparCache(); db = await dados(); desenhar(); hist();
  };
  const hist = async () => {
    const { data } = await sb.from('itens_transicoes').select('*').eq('fonte_registro', 'TELA').order('lancado_em', { ascending: false }).limit(40);
    box.querySelector('#histQ').innerHTML = data?.length ? htmlTabela(data, ['id_transicao', 'data', 'id_item', 'status_origem', 'status_destino', 'id_pessoa', 'lancado_por_email'].map((c) => ({ campo: c, titulo: c, t: 1 }))) : '<p class="nota">Nenhum movimento pelas telas ainda.</p>';
  };
  box.innerHTML = `<div class="cartao"><h3><span class="chip">B6</span> Quadro da sprint</h3>
    <p class="nota">Mova os cartões <b>na ordem do boletim</b>. Antes de cada movimento, ajuste a data, quem moveu e (para Em revisão) se houve revisão por par. Cada movimento grava uma transição (tabela 21) e atualiza o item (tabelas 14 e 20).</p>
    <form id="movForm" class="lanc"><label>Sprint<select id="spQ">${opts.sprints().map(([k, l]) => `<option value="${k}" ${k === sprintAtual ? 'selected' : ''}>${l}</option>`).join('')}</select></label>
      <label>Data do movimento<input type="date" name="data" value="2026-11-03"></label>
      <label>Quem moveu<select name="pessoa">${opts.dev().map(([k, l]) => `<option value="${k}">${l}</option>`).join('')}</select></label>
      <label>Revisão por par (só para Em revisão)<select name="rev"><option value="1">sim</option><option value="0">não</option></select></label></form>
    <div id="colunas" class="quadro" style="margin-top:10px"></div></div>
    <div class="cartao" style="margin-top:12px"><h3>Movimentos registrados pelas telas</h3><div id="histQ">…</div></div>`;
  box.querySelector('#spQ').onchange = desenhar; desenhar(); hist();
}
