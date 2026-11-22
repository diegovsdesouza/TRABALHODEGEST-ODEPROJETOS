-- 01_schema.sql · G7 Plásticos Abrantes · gerado por scripts/build_supabase.py
-- SQL Editor → New query → colar → Run. Pode rodar de novo: apaga e recria tudo.

drop table if exists public.projeto_parametros cascade;
create table public.projeto_parametros (
  id bigserial primary key,
  parametro text,
  valor text,
  unidade text,
  descricao text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.caso_de_negocio cascade;
create table public.caso_de_negocio (
  id bigserial primary key,
  ano integer,
  investimento_rs numeric,
  beneficio_bruto_rs numeric,
  custo_operacional_rs numeric,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.partes_interessadas cascade;
create table public.partes_interessadas (
  id bigserial primary key,
  id_parte text,
  parte_interessada text,
  contato text,
  papel_no_projeto text,
  tipo text,
  poder integer,
  interesse integer,
  engajamento_inicial text,
  engajamento_desejado text,
  principal_expectativa text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.equipe cascade;
create table public.equipe (
  id bigserial primary key,
  id_pessoa text,
  nome text,
  papel text,
  frente text,
  disciplina text,
  senioridade text,
  vinculo text,
  custo_hora_rs integer,
  alocacao_pct integer,
  data_entrada date,
  data_saida text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.matriz_alcadas cascade;
create table public.matriz_alcadas (
  id bigserial primary key,
  nivel_decisor text,
  limite_custo_rs numeric,
  limite_prazo_du numeric,
  pode_alterar_escopo text,
  descricao text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.eap cascade;
create table public.eap (
  id bigserial primary key,
  codigo_eap text,
  nome text,
  nivel integer,
  codigo_pai text,
  tipo_elemento text,
  disciplina text,
  id_responsavel text,
  criterio_de_aceite text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.atividades cascade;
create table public.atividades (
  id bigserial primary key,
  id_atividade text,
  codigo_eap text,
  nome_atividade text,
  disciplina text,
  tipo_atividade text,
  duracao_otimista_du numeric,
  duracao_mais_provavel_du numeric,
  duracao_pessimista_du numeric,
  duracao_fixa_du numeric,
  id_responsavel text,
  horas_internas_orcadas integer,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.dependencias cascade;
create table public.dependencias (
  id bigserial primary key,
  id_predecessora text,
  id_sucessora text,
  tipo_dependencia text,
  defasagem_du integer,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.orcamento_linha_de_base cascade;
create table public.orcamento_linha_de_base (
  id bigserial primary key,
  id_atividade text,
  categoria_custo text,
  valor_orcado_rs numeric,
  id_contrato text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.marcos cascade;
create table public.marcos (
  id bigserial primary key,
  id_marco text,
  nome_marco text,
  id_atividade text,
  regra text,
  criterio_de_aceite text,
  data_real date,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.calendario cascade;
create table public.calendario (
  id bigserial primary key,
  data date,
  dia_semana text,
  dia_util integer,
  feriado text,
  dia_util_projeto numeric,
  id_sprint text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.compressao_opcoes cascade;
create table public.compressao_opcoes (
  id bigserial primary key,
  id_atividade text,
  duracao_normal_du integer,
  duracao_minima_du integer,
  custo_adicional_por_du_rs numeric,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.epicos cascade;
create table public.epicos (
  id bigserial primary key,
  id_epico text,
  nome_epico text,
  persona text,
  beneficio_esperado text,
  id_release_planejada text,
  valor_de_negocio integer,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.backlog_itens cascade;
create table public.backlog_itens (
  id bigserial primary key,
  id_item text,
  id_epico text,
  tipo_item text,
  titulo text,
  historia_de_usuario text,
  pontos integer,
  prioridade_moscow text,
  valor_de_negocio integer,
  ordem_no_backlog integer,
  id_release text,
  origem text,
  id_mudanca text,
  id_solicitante text,
  data_criacao date,
  status text,
  id_sprint_atual text,
  id_responsavel text,
  revisao_por_par numeric,
  data_inicio date,
  data_conclusao date,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.sprints cascade;
create table public.sprints (
  id bigserial primary key,
  id_sprint text,
  numero integer,
  data_inicio date,
  data_fim date,
  dias_uteis integer,
  planejada_na_linha_de_base integer,
  id_release_alvo text,
  orcamento_sprint_rs numeric,
  pessoas_dia_disponiveis numeric,
  horas_extras_autorizadas text,
  meta_da_sprint text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.releases cascade;
create table public.releases (
  id bigserial primary key,
  id_release text,
  nome_release text,
  id_sprint_planejada text,
  data_planejada date,
  data_real date,
  objetivo text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.avanco_semanal cascade;
create table public.avanco_semanal (
  id bigserial primary key,
  semana_fim date,
  id_atividade text,
  avanco_acumulado_pct integer,
  situacao text,
  data_inicio_real date,
  data_termino_real date,
  id_responsavel text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.apontamento_horas cascade;
create table public.apontamento_horas (
  id bigserial primary key,
  semana_inicio date,
  id_pessoa text,
  tipo_item text,
  id_item text,
  horas_normais numeric,
  horas_extras numeric,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.custos_realizados cascade;
create table public.custos_realizados (
  id bigserial primary key,
  id_lancamento text,
  data date,
  frente text,
  categoria_custo text,
  id_atividade text,
  codigo_eap text,
  id_contrato text,
  id_fornecedor text,
  documento text,
  descricao text,
  valor_rs numeric,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.sprint_itens cascade;
create table public.sprint_itens (
  id bigserial primary key,
  id_sprint text,
  id_item text,
  pontos integer,
  origem_na_sprint text,
  concluido_na_sprint integer,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.itens_transicoes cascade;
create table public.itens_transicoes (
  id bigserial primary key,
  id_transicao text,
  id_item text,
  data date,
  status_origem text,
  status_destino text,
  id_pessoa text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.impedimentos cascade;
create table public.impedimentos (
  id bigserial primary key,
  id_impedimento text,
  id_item text,
  data_abertura date,
  data_fechamento date,
  tipo_impedimento text,
  dias_uteis_bloqueado integer,
  id_pessoa text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.implantacoes cascade;
create table public.implantacoes (
  id bigserial primary key,
  id_implantacao text,
  data date,
  id_sprint text,
  ambiente text,
  versao text,
  itens_implantados integer,
  tempo_ate_producao_h numeric,
  falhou integer,
  tempo_restauracao_h numeric,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.defeitos cascade;
create table public.defeitos (
  id bigserial primary key,
  id_defeito text,
  id_item_defeito text,
  id_item_origem text,
  severidade text,
  ambiente_detectado text,
  data_abertura date,
  data_resolucao date,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.inspecoes_aceite cascade;
create table public.inspecoes_aceite (
  id bigserial primary key,
  id_inspecao text,
  data date,
  id_atividade text,
  tipo_inspecao text,
  itens_verificados integer,
  itens_nao_conformes integer,
  resultado text,
  id_fornecedor text,
  horas_retrabalho numeric,
  custo_retrabalho_rs numeric,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.riscos_registro cascade;
create table public.riscos_registro (
  id bigserial primary key,
  id_risco text,
  data_identificacao date,
  tipo_risco text,
  categoria text,
  descricao text,
  causa text,
  probabilidade_pct integer,
  impacto_custo_rs numeric,
  impacto_prazo_du integer,
  frente text,
  id_atividade text,
  estrategia_resposta text,
  custo_resposta_rs numeric,
  id_responsavel text,
  status text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.riscos_ocorrencias cascade;
create table public.riscos_ocorrencias (
  id bigserial primary key,
  id_ocorrencia text,
  data date,
  id_risco text,
  descricao text,
  frente text,
  id_atividade text,
  impacto_custo_real_rs numeric,
  impacto_prazo_real_du integer,
  custo_ja_incluido_em_pagamentos text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.mudancas_solicitacoes cascade;
create table public.mudancas_solicitacoes (
  id bigserial primary key,
  id_mudanca text,
  data_abertura date,
  id_solicitante text,
  descricao text,
  tipo_mudanca text,
  frente text,
  id_atividade text,
  impacto_custo_rs numeric,
  impacto_prazo_du integer,
  impacto_pontos integer,
  status text,
  data_decisao date,
  nivel_decisor text,
  implementada text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.fornecedores cascade;
create table public.fornecedores (
  id bigserial primary key,
  id_fornecedor text,
  nome text,
  localidade text,
  categoria text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.contratos cascade;
create table public.contratos (
  id bigserial primary key,
  id_contrato text,
  id_fornecedor text,
  objeto text,
  tipo_contrato text,
  moeda text,
  valor_contratado_rs numeric,
  multa_atraso_pct_dia numeric,
  teto_multa_pct numeric,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.contratos_medicoes cascade;
create table public.contratos_medicoes (
  id bigserial primary key,
  id_medicao text,
  id_contrato text,
  id_atividade text,
  descricao_marco text,
  data_prevista date,
  valor_previsto_rs numeric,
  data_real date,
  valor_pago_rs numeric,
  aceite text,
  nao_conformidades numeric,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.propostas_fornecedores cascade;
create table public.propostas_fornecedores (
  id bigserial primary key,
  id_proposta text,
  pacote text,
  id_fornecedor text,
  preco_rs numeric,
  prazo_du integer,
  nota_tecnica numeric,
  projetos_similares integer,
  garantia_meses integer,
  condicao_pagamento text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.reunioes cascade;
create table public.reunioes (
  id bigserial primary key,
  id_reuniao text,
  data date,
  tipo_reuniao text,
  duracao_min integer,
  convidados integer,
  presentes integer,
  patrocinador_presente integer,
  decisoes_tomadas integer,
  pendencias_abertas integer,
  ata_publicada integer,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.engajamento_mensal cascade;
create table public.engajamento_mensal (
  id bigserial primary key,
  mes date,
  id_parte text,
  nivel_engajamento text,
  satisfacao numeric,
  interacoes_no_mes integer,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.pulso_equipe cascade;
create table public.pulso_equipe (
  id bigserial primary key,
  id_sprint text,
  satisfacao_media numeric,
  respostas integer,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.okr_medicoes cascade;
create table public.okr_medicoes (
  id bigserial primary key,
  id_objetivo text,
  objetivo text,
  id_resultado_chave text,
  resultado_chave text,
  unidade text,
  valor_base integer,
  meta integer,
  sentido text,
  data_medicao date,
  valor text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.funil_piloto_semanal cascade;
create table public.funil_piloto_semanal (
  id bigserial primary key,
  semana_inicio date,
  alcance integer,
  cadastros integer,
  ativados integer,
  ativos_na_semana integer,
  retidos_4_semanas integer,
  receita_rs numeric,
  indicacoes integer,
  nps integer,
  chamados_suporte integer,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.elementos_3d cascade;
create table public.elementos_3d (
  id bigserial primary key,
  id_elemento text,
  nome_elemento text,
  tipo_elemento text,
  x numeric,
  y numeric,
  z numeric,
  largura numeric,
  comprimento numeric,
  altura numeric,
  vinculo_tipo text,
  vinculo_ids text,
  ordem_de_implantacao text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.cargos_salarios cascade;
create table public.cargos_salarios (
  id bigserial primary key,
  id_pessoa text,
  vinculo text,
  remuneracao_mensal_rs integer,
  encargos_pct integer,
  beneficios_mensais_rs integer,
  horas_mensais integer,
  reajuste_previsto_pct numeric,
  mes_do_reajuste date,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.alocacao_planejada cascade;
create table public.alocacao_planejada (
  id bigserial primary key,
  id_pessoa text,
  mes date,
  horas_planejadas numeric,
  capacidade_horas numeric,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.produtividade_referencia cascade;
create table public.produtividade_referencia (
  id bigserial primary key,
  id_atividade text,
  servico text,
  unidade text,
  quantidade_total numeric,
  produtividade_planejada numeric,
  equipe_planejada_pessoas integer,
  id_contrato text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.producao_semanal cascade;
create table public.producao_semanal (
  id bigserial primary key,
  semana_fim date,
  id_atividade text,
  quantidade_executada numeric,
  hh_trabalhadas integer,
  efetivo_medio numeric,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.cenarios cascade;
create table public.cenarios (
  id bigserial primary key,
  id_cenario text,
  nome_cenario text,
  tipo_cenario text,
  descricao text,
  id_proponente text,
  variacao_beneficio_pct numeric,
  variacao_custo_operacional_anual_rs numeric,
  investimento_adicional_rs numeric,
  parcela_beneficio_antecipada_pct numeric,
  id_atividade_gatilho text,
  combinavel_com text,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.cenario_atividades cascade;
create table public.cenario_atividades (
  id bigserial primary key,
  id_cenario text,
  acao text,
  id_atividade text,
  nome_atividade text,
  disciplina text,
  duracao_du integer,
  predecessoras text,
  sucessoras text,
  custo_adicional_rs numeric,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.cenario_backlog cascade;
create table public.cenario_backlog (
  id bigserial primary key,
  id_cenario text,
  acao text,
  id_item text,
  titulo text,
  id_epico text,
  id_release text,
  pontos integer,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);
drop table if exists public.cenario_recursos cascade;
create table public.cenario_recursos (
  id bigserial primary key,
  id_cenario text,
  papel text,
  senioridade text,
  quantidade integer,
  custo_mensal_rs numeric,
  meses integer,
  ganho_velocidade_pontos_por_sprint numeric,
  sprints_de_rampa integer,
  fonte_registro text not null default 'TELA',
  lancado_por_email text default (auth.jwt() ->> 'email'),
  lancado_em timestamptz not null default now()
);

-- Regras de acesso (RLS): qualquer um lê; só integrante logado lança, edita ou apaga
alter table public.projeto_parametros enable row level security;
create policy "projeto_parametros_leitura" on public.projeto_parametros for select to anon, authenticated using (true);
create policy "projeto_parametros_escrita" on public.projeto_parametros for all to authenticated using (true) with check (true);
alter table public.caso_de_negocio enable row level security;
create policy "caso_de_negocio_leitura" on public.caso_de_negocio for select to anon, authenticated using (true);
create policy "caso_de_negocio_escrita" on public.caso_de_negocio for all to authenticated using (true) with check (true);
alter table public.partes_interessadas enable row level security;
create policy "partes_interessadas_leitura" on public.partes_interessadas for select to anon, authenticated using (true);
create policy "partes_interessadas_escrita" on public.partes_interessadas for all to authenticated using (true) with check (true);
alter table public.equipe enable row level security;
create policy "equipe_leitura" on public.equipe for select to anon, authenticated using (true);
create policy "equipe_escrita" on public.equipe for all to authenticated using (true) with check (true);
alter table public.matriz_alcadas enable row level security;
create policy "matriz_alcadas_leitura" on public.matriz_alcadas for select to anon, authenticated using (true);
create policy "matriz_alcadas_escrita" on public.matriz_alcadas for all to authenticated using (true) with check (true);
alter table public.eap enable row level security;
create policy "eap_leitura" on public.eap for select to anon, authenticated using (true);
create policy "eap_escrita" on public.eap for all to authenticated using (true) with check (true);
alter table public.atividades enable row level security;
create policy "atividades_leitura" on public.atividades for select to anon, authenticated using (true);
create policy "atividades_escrita" on public.atividades for all to authenticated using (true) with check (true);
alter table public.dependencias enable row level security;
create policy "dependencias_leitura" on public.dependencias for select to anon, authenticated using (true);
create policy "dependencias_escrita" on public.dependencias for all to authenticated using (true) with check (true);
alter table public.orcamento_linha_de_base enable row level security;
create policy "orcamento_linha_de_base_leitura" on public.orcamento_linha_de_base for select to anon, authenticated using (true);
create policy "orcamento_linha_de_base_escrita" on public.orcamento_linha_de_base for all to authenticated using (true) with check (true);
alter table public.marcos enable row level security;
create policy "marcos_leitura" on public.marcos for select to anon, authenticated using (true);
create policy "marcos_escrita" on public.marcos for all to authenticated using (true) with check (true);
alter table public.calendario enable row level security;
create policy "calendario_leitura" on public.calendario for select to anon, authenticated using (true);
create policy "calendario_escrita" on public.calendario for all to authenticated using (true) with check (true);
alter table public.compressao_opcoes enable row level security;
create policy "compressao_opcoes_leitura" on public.compressao_opcoes for select to anon, authenticated using (true);
create policy "compressao_opcoes_escrita" on public.compressao_opcoes for all to authenticated using (true) with check (true);
alter table public.epicos enable row level security;
create policy "epicos_leitura" on public.epicos for select to anon, authenticated using (true);
create policy "epicos_escrita" on public.epicos for all to authenticated using (true) with check (true);
alter table public.backlog_itens enable row level security;
create policy "backlog_itens_leitura" on public.backlog_itens for select to anon, authenticated using (true);
create policy "backlog_itens_escrita" on public.backlog_itens for all to authenticated using (true) with check (true);
alter table public.sprints enable row level security;
create policy "sprints_leitura" on public.sprints for select to anon, authenticated using (true);
create policy "sprints_escrita" on public.sprints for all to authenticated using (true) with check (true);
alter table public.releases enable row level security;
create policy "releases_leitura" on public.releases for select to anon, authenticated using (true);
create policy "releases_escrita" on public.releases for all to authenticated using (true) with check (true);
alter table public.avanco_semanal enable row level security;
create policy "avanco_semanal_leitura" on public.avanco_semanal for select to anon, authenticated using (true);
create policy "avanco_semanal_escrita" on public.avanco_semanal for all to authenticated using (true) with check (true);
alter table public.apontamento_horas enable row level security;
create policy "apontamento_horas_leitura" on public.apontamento_horas for select to anon, authenticated using (true);
create policy "apontamento_horas_escrita" on public.apontamento_horas for all to authenticated using (true) with check (true);
alter table public.custos_realizados enable row level security;
create policy "custos_realizados_leitura" on public.custos_realizados for select to anon, authenticated using (true);
create policy "custos_realizados_escrita" on public.custos_realizados for all to authenticated using (true) with check (true);
alter table public.sprint_itens enable row level security;
create policy "sprint_itens_leitura" on public.sprint_itens for select to anon, authenticated using (true);
create policy "sprint_itens_escrita" on public.sprint_itens for all to authenticated using (true) with check (true);
alter table public.itens_transicoes enable row level security;
create policy "itens_transicoes_leitura" on public.itens_transicoes for select to anon, authenticated using (true);
create policy "itens_transicoes_escrita" on public.itens_transicoes for all to authenticated using (true) with check (true);
alter table public.impedimentos enable row level security;
create policy "impedimentos_leitura" on public.impedimentos for select to anon, authenticated using (true);
create policy "impedimentos_escrita" on public.impedimentos for all to authenticated using (true) with check (true);
alter table public.implantacoes enable row level security;
create policy "implantacoes_leitura" on public.implantacoes for select to anon, authenticated using (true);
create policy "implantacoes_escrita" on public.implantacoes for all to authenticated using (true) with check (true);
alter table public.defeitos enable row level security;
create policy "defeitos_leitura" on public.defeitos for select to anon, authenticated using (true);
create policy "defeitos_escrita" on public.defeitos for all to authenticated using (true) with check (true);
alter table public.inspecoes_aceite enable row level security;
create policy "inspecoes_aceite_leitura" on public.inspecoes_aceite for select to anon, authenticated using (true);
create policy "inspecoes_aceite_escrita" on public.inspecoes_aceite for all to authenticated using (true) with check (true);
alter table public.riscos_registro enable row level security;
create policy "riscos_registro_leitura" on public.riscos_registro for select to anon, authenticated using (true);
create policy "riscos_registro_escrita" on public.riscos_registro for all to authenticated using (true) with check (true);
alter table public.riscos_ocorrencias enable row level security;
create policy "riscos_ocorrencias_leitura" on public.riscos_ocorrencias for select to anon, authenticated using (true);
create policy "riscos_ocorrencias_escrita" on public.riscos_ocorrencias for all to authenticated using (true) with check (true);
alter table public.mudancas_solicitacoes enable row level security;
create policy "mudancas_solicitacoes_leitura" on public.mudancas_solicitacoes for select to anon, authenticated using (true);
create policy "mudancas_solicitacoes_escrita" on public.mudancas_solicitacoes for all to authenticated using (true) with check (true);
alter table public.fornecedores enable row level security;
create policy "fornecedores_leitura" on public.fornecedores for select to anon, authenticated using (true);
create policy "fornecedores_escrita" on public.fornecedores for all to authenticated using (true) with check (true);
alter table public.contratos enable row level security;
create policy "contratos_leitura" on public.contratos for select to anon, authenticated using (true);
create policy "contratos_escrita" on public.contratos for all to authenticated using (true) with check (true);
alter table public.contratos_medicoes enable row level security;
create policy "contratos_medicoes_leitura" on public.contratos_medicoes for select to anon, authenticated using (true);
create policy "contratos_medicoes_escrita" on public.contratos_medicoes for all to authenticated using (true) with check (true);
alter table public.propostas_fornecedores enable row level security;
create policy "propostas_fornecedores_leitura" on public.propostas_fornecedores for select to anon, authenticated using (true);
create policy "propostas_fornecedores_escrita" on public.propostas_fornecedores for all to authenticated using (true) with check (true);
alter table public.reunioes enable row level security;
create policy "reunioes_leitura" on public.reunioes for select to anon, authenticated using (true);
create policy "reunioes_escrita" on public.reunioes for all to authenticated using (true) with check (true);
alter table public.engajamento_mensal enable row level security;
create policy "engajamento_mensal_leitura" on public.engajamento_mensal for select to anon, authenticated using (true);
create policy "engajamento_mensal_escrita" on public.engajamento_mensal for all to authenticated using (true) with check (true);
alter table public.pulso_equipe enable row level security;
create policy "pulso_equipe_leitura" on public.pulso_equipe for select to anon, authenticated using (true);
create policy "pulso_equipe_escrita" on public.pulso_equipe for all to authenticated using (true) with check (true);
alter table public.okr_medicoes enable row level security;
create policy "okr_medicoes_leitura" on public.okr_medicoes for select to anon, authenticated using (true);
create policy "okr_medicoes_escrita" on public.okr_medicoes for all to authenticated using (true) with check (true);
alter table public.funil_piloto_semanal enable row level security;
create policy "funil_piloto_semanal_leitura" on public.funil_piloto_semanal for select to anon, authenticated using (true);
create policy "funil_piloto_semanal_escrita" on public.funil_piloto_semanal for all to authenticated using (true) with check (true);
alter table public.elementos_3d enable row level security;
create policy "elementos_3d_leitura" on public.elementos_3d for select to anon, authenticated using (true);
create policy "elementos_3d_escrita" on public.elementos_3d for all to authenticated using (true) with check (true);
alter table public.cargos_salarios enable row level security;
create policy "cargos_salarios_leitura" on public.cargos_salarios for select to anon, authenticated using (true);
create policy "cargos_salarios_escrita" on public.cargos_salarios for all to authenticated using (true) with check (true);
alter table public.alocacao_planejada enable row level security;
create policy "alocacao_planejada_leitura" on public.alocacao_planejada for select to anon, authenticated using (true);
create policy "alocacao_planejada_escrita" on public.alocacao_planejada for all to authenticated using (true) with check (true);
alter table public.produtividade_referencia enable row level security;
create policy "produtividade_referencia_leitura" on public.produtividade_referencia for select to anon, authenticated using (true);
create policy "produtividade_referencia_escrita" on public.produtividade_referencia for all to authenticated using (true) with check (true);
alter table public.producao_semanal enable row level security;
create policy "producao_semanal_leitura" on public.producao_semanal for select to anon, authenticated using (true);
create policy "producao_semanal_escrita" on public.producao_semanal for all to authenticated using (true) with check (true);
alter table public.cenarios enable row level security;
create policy "cenarios_leitura" on public.cenarios for select to anon, authenticated using (true);
create policy "cenarios_escrita" on public.cenarios for all to authenticated using (true) with check (true);
alter table public.cenario_atividades enable row level security;
create policy "cenario_atividades_leitura" on public.cenario_atividades for select to anon, authenticated using (true);
create policy "cenario_atividades_escrita" on public.cenario_atividades for all to authenticated using (true) with check (true);
alter table public.cenario_backlog enable row level security;
create policy "cenario_backlog_leitura" on public.cenario_backlog for select to anon, authenticated using (true);
create policy "cenario_backlog_escrita" on public.cenario_backlog for all to authenticated using (true) with check (true);
alter table public.cenario_recursos enable row level security;
create policy "cenario_recursos_leitura" on public.cenario_recursos for select to anon, authenticated using (true);
create policy "cenario_recursos_escrita" on public.cenario_recursos for all to authenticated using (true) with check (true);

grant usage on schema public to anon, authenticated;
grant select on all tables in schema public to anon, authenticated;
grant insert, update, delete on all tables in schema public to authenticated;
grant usage, select on all sequences in schema public to authenticated;
