"""Rascunhos dos documentos D1 a D17 (Parte 1), com os números do sistema na data de status.

Uso: python scripts/documentos.py dados/tratados /tmp/snap.json docs/documentos
(/tmp/snap.json = fotografia gerada por testes/snapshot.mjs, com os boletins lançados)
Gera um .md por documento (editável no GitHub) e o PDF correspondente.
"""
import os, sys, json, math, subprocess
import pandas as pd, markdown

src, snapf, out = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(out, exist_ok=True)
S = json.load(open(snapf))
def r(n):
    """Lê a tabela do banco local de teste (com os boletins lançados pelas telas); se o banco não estiver ligado, lê o CSV tratado."""
    tab = n.split('_', 1)[1]
    try:
        js = subprocess.run(['psql', '-h', '/tmp/pgt', '-p', '5499', '-U', 'postgres', '-tAc',
                             f"select coalesce(json_agg(_r),'[]') from (select * from {tab} order by id) _r"], capture_output=True, text=True, check=True).stdout
        df = pd.DataFrame(json.loads(js)).drop(columns=['id', 'fonte_registro', 'lancado_por_email', 'lancado_em'], errors='ignore')
        for c in ('codigo_eap', 'codigo_pai'):
            if c in df: df[c] = df[c].astype('string')
        return df
    except Exception:
        return pd.read_csv(f'{src}/{n}.csv', dtype={'codigo_eap': str, 'codigo_pai': str})
def br(v, d=0):
    if v is None or (isinstance(v, float) and math.isnan(v)): return '—'
    return f'{v:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
rs = lambda v: 'R$ ' + br(v); pc = lambda v, d=1: br(v * 100, d) + '%'
dt = lambda s: '/'.join(reversed(str(s).split('-'))) if isinstance(s, str) and len(s) == 10 else (s or '—')
def T(cab, linhas): return '| ' + ' | '.join(cab) + ' |\n|' + '---|' * len(cab) + '\n' + '\n'.join('| ' + ' | '.join(str(c) for c in l) + ' |' for l in linhas) + '\n'

atv = r('07_atividades'); eap = r('06_eap'); eq = r('04_equipe'); orc = r('09_orcamento_linha_de_base'); pi = r('03_partes_interessadas'); bl = r('14_backlog_itens')
ep = r('13_epicos'); sp = r('15_sprints'); rel = r('16_releases'); rk = r('26_riscos_registro'); oc = r('27_riscos_ocorrencias'); sm = r('28_mudancas_solicitacoes')
ct = r('30_contratos'); fo = r('29_fornecedores'); ins = r('25_inspecoes_aceite'); dfe = r('24_defeitos'); imp = r('23_implantacoes'); impd = r('22_impedimentos')
reu = r('33_reunioes'); eng = r('34_engajamento_mensal'); pul = r('35_pulso_equipe'); okr = r('36_okr_medicoes'); fun = r('37_funil_piloto_semanal'); al = r('05_matriz_alcadas')
cn = r('02_caso_de_negocio'); par = r('01_projeto_parametros'); aloc = r('40_alocacao_planejada'); el = r('38_elementos_3d'); cen = r('43_cenarios'); mar = r('10_marcos')
nomeP = dict(zip(eq.id_pessoa, eq.nome)); nomeA = dict(zip(atv.id_atividade, atv.nome_atividade)); nomeE = dict(zip(eap.codigo_eap, eap.nome)); nomePI = dict(zip(pi.id_parte, pi.parte_interessada))
EV = S['ev']; PJ = EV['projeto']; PV = S['pv']; LB = S['lb']; AG = PV['agil']; C1 = next(c for c in S['cen'] if c['id'] == 'C1')
CEN = {c['id']: c for c in S['cen']}; MELHOR = max(S['cen'], key=lambda c: c['resultado'])
DOCS = {}

def doc(cod, titulo, dono, fontes, corpo):
    DOCS[cod] = (titulo, dono, f'''# {cod} · {titulo}

**Projeto:** Linha de injeção e pintura de para-choques · Plásticos Abrantes (G7) · ENGN62 2026.2
**Versão:** 0.1 (rascunho) · **Data de status:** 13/11/2026 · **Responsável:** {dono} · **Revisão:** ____________
**Fontes:** {fontes}

{corpo.strip()}

---
*Rascunho gerado a partir dos números do sistema (https://trabalhodegest-odeprojetos.netlify.app, data de corte 13/11/2026, com os boletins B1 a B10 lançados). O responsável revisa, completa os campos em branco, ajusta o texto e assina.*
''')

# ------------------------------------------------------------ D1
base = cn.sort_values('ano'); fl = (base.beneficio_bruto_rs - base.custo_operacional_rs.where(base.ano > 0, 0) - base.investimento_rs).tolist()
vpl0 = sum(f / 1.14 ** a for a, f in zip(base.ano, fl)); ac = 0; pb = None
for a, f in zip(base.ano, fl):
    antes = ac; ac += f
    if pb is None and antes < 0 <= ac: pb = a - 1 + (-antes / f)
mk = [[m.id_marco, m.nome_marco, m.id_atividade, dt(LB['ativ'][m.id_atividade]['termino']), dt(PV['ativ'][m.id_atividade]['termino'])] for m in mar.itertuples()]
doc('D1', 'Termo de abertura e caso de negócio', 'José', 'tabelas 01, 02, 03 e 10; dossiê (ficha do projeto); convenção 16', f'''
## 1. Termo de abertura

| Item | Conteúdo |
|---|---|
| Nome | Implantação da linha de injeção e pintura de para-choques |
| Patrocinador | Ramon Jesus, diretor de operações (PI01) |
| Gerente do projeto | {nomeP['P01']} (P01) |
| Objetivo | Aprovar as peças no cliente e iniciar o fornecimento em série na data contratual, com refugo de pintura abaixo de 6% na partida |
| Justificativa | Contrato de fornecimento de para-choques com uma montadora; a capacidade atual (Linha de painéis) não atende o novo produto |
| Início | 02/02/2026 (dia útil 1) |
| Término contratual | 07/05/2027 (du 312); cada dia útil de atraso custa R$ 50.100 |
| Orçamento (ONT) | {rs(PJ['ont'])} = preditiva R$ 38.271.476 + ágil R$ 737.800 |
| Reservas | contingência R$ 831.000 (gerente) · gerencial R$ 1.170.000 (patrocinador) |

**Escopo (duas frentes):**
- **Preditiva:** engenharia e licenças; compra e importação da injetora de 3.200 t, da cabine de pintura robotizada e do transportador aéreo com robôs; obra civil e utilidades; elétrica e automação; montagem; NR-12; comissionamento, testes (FAT, SAT) e partida; treinamento.
- **Ágil:** sistemas digitais da linha (coleta de dados, painel de desempenho, rastreabilidade, receitas e manutenção), em 3 releases.

**Fora do escopo:** _(completar: ex. ampliação do galpão, outros produtos, integração com o ERP da montadora)_.

**Premissas e restrições:** a Linha de painéis continua operando durante a obra; a injetora é importada (câmbio em euro); a Release 2 precisa estar pronta para o teste de aceite em campo (A47) e a Release 3 para o aceite final (A56).

**Critérios de sucesso:** término até 07/05/2027; custo dentro do ONT + reservas; refugo de pintura < 6% na partida; releases aceitas pelo cliente.

## 2. Marcos

{T(['Marco', 'Nome', 'Atividade', 'Linha de base', 'Previsão em 13/11'], mk)}

## 3. Caso de negócio (tabela 02, TMA 14% a.a.)

{T(['Ano', 'Investimento', 'Benefício bruto', 'Custo operacional', 'Fluxo líquido', 'Valor presente'], [[a.ano, br(a.investimento_rs), br(a.beneficio_bruto_rs), br(a.custo_operacional_rs if a.ano else 0), br(f), br(f / 1.14 ** a.ano)] for a, f in zip(base.itertuples(), fl)])}

- **VPL do plano original:** {rs(vpl0)} · **payback simples:** {br(pb, 2)} anos (convenção 16).
- **VPL hoje (cenário C1, com a ENT de {rs(C1['ent'])} e {br(C1['meses'], 2)} mês de atraso):** {rs(C1['vpl'])} · payback {br(C1['payback'], 2)} anos.

**Leitura:** o projeto se paga em pouco mais de 4 anos e continua atrativo, mas o estouro de custo (+{rs(C1['ent'] - PJ['ont'])}) já consumiu {pc(1 - C1['vpl'] / vpl0, 0)} do VPL original.
''')

# ------------------------------------------------------------ D2
ult = eng[eng.mes == eng.mes.max()].set_index('id_parte')
nv = ['DESCONHECE', 'RESISTENTE', 'NEUTRO', 'APOIA', 'LIDERA']
q = lambda po, it: 'Gerenciar de perto' if po >= 4 and it >= 4 else 'Manter satisfeito' if po >= 4 else 'Manter informado' if it >= 4 else 'Monitorar'
lin2 = [[p.id_parte, p.parte_interessada, p.poder, p.interesse, q(p.poder, p.interesse), p.engajamento_inicial, ult.nivel_engajamento.get(p.id_parte, '—'), p.engajamento_desejado, br(ult.satisfacao.get(p.id_parte), 1)] for p in pi.itertuples()]
gr = reu.groupby('tipo_reuniao').agg(n=('id_reuniao', 'count'), pres=('presentes', 'sum'), conv=('convidados', 'sum'), atas=('ata_publicada', 'sum'), pat=('patrocinador_presente', 'sum'), dec=('decisoes_tomadas', 'sum'), pend=('pendencias_abertas', 'sum'))
doc('D2', 'Partes interessadas e comunicação', 'Arley', 'tabelas 03, 33 e 34 (com o boletim B9)', f'''
## 1. Registro e estratégia (poder × interesse; alto = 4 ou 5)

{T(['Id', 'Parte', 'Poder', 'Interesse', 'Estratégia', 'Inicial', 'Atual (nov/26)', 'Desejado', 'Satisfação'], lin2)}

**Destaques:**
- **PI13 · engenharia da montadora:** RESISTENTE, satisfação 2,8. É quem pede mudanças direto ao time ágil (8 pedidos diretos, 22 pontos, sem solicitação de mudança). Ação: canal único pelo controle de mudanças (D11) e reunião quinzenal com o gerente do projeto.
- **PI01 · patrocinador:** caiu para NEUTRO (5,9) e esteve ausente do último comitê diretor (12/11). Ação: relatório executivo curto antes de cada comitê, com a decisão pedida.
- _(completar: ações para as demais partes abaixo do desejado)_

## 2. Plano de comunicação (reuniões realizadas)

{T(['Reunião', 'Quantas', 'Presença média', 'Atas publicadas', 'Patrocinador presente', 'Decisões', 'Pendências abertas'], [[k, g.n, pc(g.pres / g.conv, 0), f'{g.atas}/{g.n}', g.pat, g.dec, g.pend] for k, g in gr.iterrows()])}

| Comunicação | Público | Frequência | Responsável | Meio |
|---|---|---|---|---|
| Status semanal | equipe, fornecedores-chave | semanal | gerente do projeto | reunião + ata |
| Comitê diretor | patrocinador, diretoria, cliente | mensal | gerente do projeto | reunião + relatório executivo |
| Cerimônias ágeis | time ágil, dono do produto | por sprint | Scrum Master | Jira + reunião |
| Relatório ao cliente | engenharia da montadora | quinzenal | gerente do projeto | relatório + reunião |
| _(completar)_ | | | | |
''')

# ------------------------------------------------------------ D3
orcA = orc.groupby('id_atividade').valor_orcado_rs.sum()
pac = eap[eap.nivel == 3]
lin3 = []
for p in pac.itertuples():
    a = atv[atv.codigo_eap == p.codigo_eap]
    lin3.append([p.codigo_eap, p.nome, f'{p.id_responsavel} {nomeP.get(p.id_responsavel, "")}', ', '.join(a.id_atividade), br(orcA.reindex(a.id_atividade).fillna(0).sum()), '_(critério de aceite)_'])
ent = eap[eap.nivel == 2]
arv = '\n'.join(f'- **{e.codigo_eap} {e.nome}**\n' + '\n'.join(f'  - {p.codigo_eap} {p.nome}' for p in pac[pac.codigo_pai == e.codigo_eap].itertuples()) for e in ent.itertuples())
doc('D3', 'EAP e dicionário da EAP', 'Caique', 'tabelas 04, 06, 07 e 09', f'''
## 1. EAP (projeto → 8 entregas → 22 pacotes)

- **1 Linha de injeção e pintura de para-choques**
{arv}

Regra: entregas e pacotes são **substantivos** (o que se entrega); as atividades (tabela 07) começam com **verbo no infinitivo**.

## 2. Dicionário da EAP

{T(['Pacote', 'Nome', 'Responsável', 'Atividades', 'Orçamento (R$)', 'Critério de aceite'], lin3)}

## 3. Regra dos 100%

Soma do orçamento dos pacotes e entregas = **R$ {br(orc.valor_orcado_rs.sum())}** = ONT da frente preditiva (R$ 38.271.476) ✔. A frente ágil (R$ 737.800) é orçada por sprint (tabela 15).
''')

# ------------------------------------------------------------ D4
lin4 = [[i, nomeA[i], LB['dur'][i], dt(LB['ativ'][i]['inicio']), dt(LB['ativ'][i]['termino']), LB['ativ'][i]['folga'], 'sim' if LB['ativ'][i]['critica'] else '', PV['ativ'][i]['situacao'].replace('_', ' ').lower(), dt(PV['ativ'][i]['termino']), PV['ativ'][i]['desvio']]
        for i in sorted(LB['ativ'], key=lambda k: (LB['ativ'][k]['ES'], k))]
doc('D4', 'Cronograma (ProjectLibre)', 'Caique', 'tabelas 07, 08, 11 e 17; convenções 1, 2 e 11; arquivos docs/projectlibre/', f'''
## 1. Como foi montado

1. Calendário de segunda a sexta, 8 h/dia, com os feriados da tabela 11.
2. EAP como tarefas-resumo; as 59 atividades dentro dos pacotes.
3. Duração = ⌈(O + 4M + P) ÷ 6⌉ (convenção 1); marcos ágeis com duração fixa.
4. 88 ligações: TI = término-início (FS), II = início-início (SS), com defasagem em dias úteis (convenção 2).
5. Linha de base salva; avanço real lançado na data de status 13/11/2026.

Arquivos: `cronograma_G7.pod` e `gantt_G7.pdf` em `docs/projectlibre/` _(Caique: anexar)_.

## 2. Resultado

| Item | Linha de base | Previsão em 13/11 |
|---|---|---|
| Término | {dt(LB['termino'])} (du {LB['fim']}) | **{dt(PV['termino'])}** (du {PV['fim']}) |
| Folga até o contrato (07/05/2027) | 8 du | **−{PV['du']} du** (custo {rs(PV['custoAtraso'])}) |
| Caminho crítico / cadeia do término | A01 → A07 → A08 → A09 → A11 → A12 → A13 → A38 → A41 → A43 → A44 → A46 → A47 → A49 → A56 | {' → '.join(PV['cadeia'])} |

**Conferência com o sistema e com o papel:** o término e o caminho crítico do ProjectLibre devem ser os mesmos do sistema (página Prazo) e da folha M1 (sub-rede). _(Caique: anotar aqui o que o ProjectLibre mostrou)_

## 3. Tabela da rede

{T(['Ativ.', 'Nome', 'Dur.', 'Início LB', 'Término LB', 'Folga', 'Crítica', 'Situação', 'Término previsto', 'Desvio (du)'], lin4)}
''')

# ------------------------------------------------------------ D5
oc5 = orc.merge(atv[['id_atividade', 'codigo_eap']]); oc5['entrega'] = oc5.codigo_eap.str.split('.').str[:2].str.join('.')
piv = oc5.pivot_table(index='entrega', columns='categoria_custo', values='valor_orcado_rs', aggfunc='sum', fill_value=0)
lin5 = [[k, nomeE.get(k, ''), *[br(v) for v in row], br(row.sum())] for k, row in piv.iterrows()]
lin5.append(['', '**Total**', *[f'**{br(v)}**' for v in piv.sum()], f'**{br(piv.values.sum())}**'])
ms = [[dt(m['mes']), br(m['vp'] / 1000, 1), br(m['va'] / 1000, 1) if m['va'] is not None else '', br(m['cr'] / 1000, 1) if m['cr'] is not None else ''] for m in S['meses']]
doc('D5', 'Orçamento, curva S e reservas', 'José', 'tabelas 01, 02, 09, 15, 17, 18 e 19; convenções 4 a 7', f'''
## 1. Orçamento por entrega e categoria (frente preditiva, R$)

{T(['Entrega', 'Nome', *piv.columns, 'Total'], lin5)}

Frente ágil: 17 sprints × R$ 43.400 = R$ 737.800. **ONT do projeto = {rs(PJ['ont'])}.**

## 2. Curva S (R$ mil, acumulado no fim do mês, duas frentes)

{T(['Mês', 'VP', 'VA', 'CR'], ms)}

Conferência: em 25/09/2026, VP 32.721,8 · VA 30.395,7 · CR 30.119,3 (dossiê) ✔ (folha M3).

## 3. Situação em 13/11/2026

VP {rs(PJ['vp'])} · VA {rs(PJ['va'])} · CR {rs(PJ['cr'])} · IDP {br(PJ['idp'], 3)} · IDC {br(PJ['idc'], 3)} · **ENT {rs(PJ['ent'])}** (desvio {rs(PJ['ent'] - PJ['ont'])}) · IDPT {br(PJ['idpt'], 2)}.

## 4. Reservas e orçamento total

| Componente | R$ |
|---|---|
| Linha de base de custo (ONT) | {br(PJ['ont'])} |
| Contingência (riscos identificados) | 831.000 |
| Reserva gerencial (não identificados) | 1.170.000 |
| Gestão do projeto (indiretos, R$ 85.800/mês × 15 meses) | {br(85800 * 15)} _(conferir o prazo usado)_ |
| **Total** | **{br(PJ['ont'] + 831000 + 1170000 + 85800 * 15)}** _(comparar com o investimento do ano 0 do caso de negócio: R$ 43.007.000)_ |

**Consumo das reservas até 13/11:** contingência {rs(S['reservas']['contingenciaUsada'])} de R$ 831.000 (saldo **{rs(S['reservas']['contingenciaSaldo'])}**); gerencial {rs(S['reservas']['gerencialUsada'])} (saldo {rs(S['reservas']['gerencialSaldo'])}).
''')

# ------------------------------------------------------------ D6
mesC = aloc.assign(m=aloc.mes.str[:7]).groupby('m').horas_planejadas.sum()
sup = aloc[aloc.horas_planejadas > aloc.capacidade_horas]
raci = []
for e in ent.itertuples():
    resp = sorted(set(pac[pac.codigo_pai == e.codigo_eap].id_responsavel.dropna()) | set(eap[eap.codigo_eap == e.codigo_eap].id_responsavel.dropna()))
    raci.append([f'{e.codigo_eap} {e.nome}', ', '.join(f'{x} {nomeP.get(x, "")}' for x in resp) or '_(definir)_', 'P01 ' + nomeP['P01'], '_(qualidade, SESMT, fornecedor)_', 'PI01 patrocinador, PI13 cliente'])
doc('D6', 'Matriz RACI e histograma de recursos', 'Arley', 'tabelas 04, 06, 18 e 40; convenção 18', f'''
## 1. RACI por entrega

R = executa · A = responde (um só por linha) · C = consultado · I = informado

{T(['Entrega', 'R (executa)', 'A (responde)', 'C (consultado)', 'I (informado)'], raci)}

## 2. Histograma de horas planejadas (equipe interna, tabela 40)

{T(['Mês', 'Horas planejadas'], [[k, br(v, 1)] for k, v in mesC.items()])}

**Superalocação no plano:** {'; '.join(f"{x.id_pessoa} {nomeP[x.id_pessoa]} em {x.mes[:7]}: {br(x.horas_planejadas, 1)} h para {br(x.capacidade_horas, 0)} h de capacidade" for x in sup.itertuples()) or 'nenhuma'}. Ação: nivelar movendo horas para o mês seguinte ou dividir com outro comprador.

**Planejado × apontado:** ver D13 (desvios acima de 20% por pessoa e mês). _(Arley: inserir o gráfico do histograma do sistema, página Pessoas)_
''')

# ------------------------------------------------------------ D7
epl = []
for e in ep.itertuples():
    it = bl[bl.id_epico == e.id_epico]; epl.append([e.id_epico, e.nome_epico, e.id_release_planejada, len(it), it.pontos.sum(), it[it.status == 'CONCLUIDO'].pontos.sum()])
rl = [[k, dt(v['planejada']), dt(v['real']) if v['real'] else '—', v['pontosRestantes'], v['sprints'], v['sprint'] if v['sprints'] else '—', dt(v['data'])] for k, v in AG['releases'].items()]
doc('D7', 'Backlog e releases no Jira', 'Guilherme', 'tabelas 13 a 16 e 20; convenções 8 e 10; Jira', f'''
## 1. Jira

- Projeto Scrum: _(link)_ · professor convidado: _(sim/data)_
- Backlog importado de `docs/jira/backlog_jira.csv` (5 épicos, 94 itens); versões R1, R2 e R3; sprint S14 executada no quadro na ordem do boletim B6.
- Capturas: burndown da S14 e relatório de velocidade em `docs/jira/` _(anexar)_.

## 2. Backlog por épico (em 30/10, antes da S14)

{T(['Épico', 'Nome', 'Release', 'Itens', 'Pontos', 'Pontos concluídos'], epl)}

Prioridade MoSCoW: MUST = sem isso a release não sai; SHOULD = importante; COULD = desejável; WONT = fora desta versão.

## 3. Plano de releases (convenção 10)

Velocidade média das 5 últimas sprints (S10 a S14): **{br(AG['vmed'], 1)} pontos/sprint** ({', '.join(f"{s}={AG['vel'].get(s, 0)}" for s in AG['ult5'])}).

{T(['Release', 'Planejada', 'Real', 'Pontos restantes', 'Sprints', 'Fim previsto na', 'Data prevista'], rl)}

**MVP:** a Release 2 (coleta de dados + rastreabilidade) é o mínimo para o teste de aceite em campo (A47). **Leitura:** a R2 atrasou 47 du por causa de transbordos e pedidos diretos; ela ainda não define o término do projeto, mas a folga até o A47 é a próxima a ser consumida.
''')

# ------------------------------------------------------------ D8
vel = [[s.id_sprint, dt(s.data_inicio), dt(s.data_fim), s.pontos_comprometidos if 'pontos_comprometidos' in sp.columns else '—', AG['vel'].get(s.id_sprint, 0)] for s in sp.itertuples() if s.data_fim <= '2026-11-13']
dora = imp[imp.ambiente == 'PRODUCAO']; sem = (pd.Timestamp('2026-11-13') - pd.Timestamp('2026-05-04')).days / 7
doc('D8', 'Rotina ágil e métricas', 'Guilherme', 'tabelas 15, 20 a 24, 33, 35 e 37; convenções 8, 9 e 13', f'''
## 1. Rotina

Sprints de 2 semanas desde 04/05/2026. Cerimônias: planejamento da sprint, reunião diária, revisão, retrospectiva; status semanal com a gestão. Quadro: A FAZER → EM ANDAMENTO → EM REVISÃO → EM TESTE → CONCLUÍDO.

## 2. Velocidade

{T(['Sprint', 'Início', 'Fim', 'Comprometido', 'Concluído (pt)'], vel)}

Média das 5 últimas: **{br(AG['vmed'], 1)} pt/sprint**.

## 3. Fluxo

| Sprint | Pontos | Velocidade | Ciclo médio (du) | Vazão (itens/du) | WIP (Little) |
|---|---|---|---|---|---|
| S13 | {S['bd13']['total']} | {S['bd13']['vel']} | {br(S['fl13']['ciclo'], 2)} | {br(S['fl13']['vazao'], 2)} | {br(S['fl13']['ciclo'] * S['fl13']['vazao'], 1)} |
| S14 | {S['bd14']['total']} | {S['bd14']['vel']} | {br(S['fl14']['ciclo'], 2)} | {br(S['fl14']['vazao'], 2)} | {br(S['fl14']['ciclo'] * S['fl14']['vazao'], 1)} |

Burndown S14 (restantes no fim de cada du): {', '.join(map(str, S['bd14']['rest']))}.

## 4. DORA, qualidade e equipe

- Implantações em produção: {len(dora)} em {br(sem, 1)} semanas → **{br(len(dora) / sem, 2)}/semana**; taxa de falha **{pc((dora.falhou == 1).mean(), 0)}**; restauração média {br(dora[dora.falhou == 1].tempo_restauracao_h.mean(), 1)} h; lead time mediano {br(dora.tempo_ate_producao_h.median(), 1)} h (convenção 13).
- Defeitos abertos: {len(dfe)} no total, {int((dfe.data_resolucao.isna() & ~dfe.id_item_defeito.isin(bl[bl.status == 'CONCLUIDO'].id_item)).sum())} sem resolução (defeito resolvido quando o item de correção está concluído). Impedimentos: {len(impd)}, {int(impd.data_fechamento.isna().sum())} abertos.
- Pulso da equipe: {', '.join(f"{p.id_sprint}={br(p.satisfacao_media, 2)}" for p in pul.tail(5).itertuples())} (escala 1 a 5).
- Funil do piloto: _(resumir a tabela 37: alcance, ativação, retenção, NPS)_.

**Leitura:** {pc((dora.falhou == 1).mean(), 0)} de falha nas implantações e itens entrando no meio da sprint explicam a velocidade instável. Ações: definição de pronto com teste automatizado; proteger a sprint de pedidos diretos.
''')

# ------------------------------------------------------------ D9
RK = S['riscos']; RE = S['reservas']
lin9 = [[x['id_risco'], x['descricao'], x['categoria'], x['probabilidade_pct'], br(x['impacto_custo_rs']), x['impacto_prazo_du'], br(x['vme']), x['estrategia_resposta'], x['id_responsavel']] for x in RK['abertas']]
lin9b = [[o['id_ocorrencia'], dt(o['data']), o['id_risco'] or 'imprevisto', o['descricao'], br(o['impacto_custo_real_rs']), o['impacto_prazo_real_du']] for o in RE['ocorrencias']]
doc('D9', 'Riscos e reservas', 'Marjorie', 'tabelas 01, 26 e 27; convenção 12; folha M6', f'''
## 1. Ameaças abertas (convenção 12: VME = probabilidade × impacto)

{T(['Id', 'Risco', 'Categoria', 'Prob. (%)', 'Impacto (R$)', 'Prazo (du)', 'VME (R$)', 'Resposta', 'Dono'], lin9)}

**Exposição total:** {rs(RK['exposicao'])}. A matriz 5 × 5 está na folha M6 e no sistema (página Riscos e mudanças).

## 2. Ocorrências e consumo das reservas

{T(['Id', 'Data', 'Risco', 'Descrição', 'Custo (R$)', 'Prazo (du)'], lin9b)}

| Reserva | Valor | Consumido | Saldo |
|---|---|---|---|
| Contingência | R$ 831.000 | {rs(RE['contingenciaUsada'])} | **{rs(RE['contingenciaSaldo'])}** |
| Gerencial | R$ 1.170.000 | {rs(RE['gerencialUsada'])} | {rs(RE['gerencialSaldo'])} |

**A reserva cobre os riscos abertos? Não.** A contingência já está negativa em {rs(-RE['contingenciaSaldo'])} (o câmbio da injetora, R15, consumiu R$ 812 mil sozinho), e ainda há {rs(RK['exposicao'])} de exposição. Será preciso pedir ao patrocinador o remanejamento da reserva gerencial ou um aditivo de {rs(RK['exposicao'] - RE['contingenciaSaldo'])}.

## 3. Respostas para os 5 maiores riscos

_(Marjorie: para cada um, a resposta concreta, o custo da resposta, o dono e o gatilho de acompanhamento. Ex.: R13 cabine fora do padrão → mitigar com teste de aparência no FAT e painel-padrão aprovado pela montadora.)_
''')

# ------------------------------------------------------------ D10
CT = S['contratos']
lin10 = [[c['id_contrato'], c['fornecedor'], c['objeto'], c['tipo_contrato'], br(c['valor_contratado_rs']), f"{c['pagas']}/{c['medicoes']}", br(c['pago']), br(c['desvioPago']), c['atrasoUltimoMarco'], br(c['multa'])] for c in CT]
sel = [[p['id_proposta'], p['fornecedor'], br(p['preco_rs']), *[br(p['n_' + k], 3) for k in ['preco', 'tecnica', 'prazo', 'experiencia', 'garantia']], f"**{br(p['nota'], 3)}**"] for p in S['selecao']]
q10 = ins.groupby(ins.id_fornecedor.fillna('—')).agg(n=('id_inspecao', 'count'), nc=('itens_nao_conformes', 'sum'), it=('itens_verificados', 'sum'), rep=('resultado', lambda x: (x == 'REPROVADO').sum()), custo=('custo_retrabalho_rs', 'sum'))
fn = dict(zip(fo.id_fornecedor, fo.nome))
doc('D10', 'Aquisições e qualidade', 'Marjorie', 'tabelas 25, 29 a 32 e 24; convenções 14 e 15', f'''
## 1. Contratos

{T(['Contrato', 'Fornecedor', 'Objeto', 'Tipo', 'Valor (R$)', 'Medições pagas', 'Pago (R$)', 'Pago − previsto', 'Atraso último marco (dias)', 'Multa (R$)'], lin10)}

- **Desvios:** CT03 injetora (contrato em euro): +R$ 812.232 de câmbio (risco R15). CT07 obra civil (preço unitário): todas as medições 5% a 9% acima do previsto, +R$ 291.061 (quantidade medida maior que a orçada).
- **Multas por atraso (convenção 14):** total {rs(sum(c['multa'] for c in CT))} a cobrar ({', '.join(c['id_contrato'] for c in CT if c['multa'] > 0)}). _(Marjorie: justificar o tipo de contrato de cada fornecedor.)_

## 2. Seleção do fornecedor de comissionamento elétrico (convenção 15)

{T(['Proposta', 'Fornecedor', 'Preço', 'Preço', 'Técnica', 'Prazo', 'Experiência', 'Garantia', 'Nota'], sel)}

Pesos: preço 35%, técnica 30%, prazo 15%, experiência 10%, garantia 10%. **Recomendação: {S['selecao'][0]['id_proposta']} ({S['selecao'][0]['fornecedor']})**.

## 3. Qualidade (inspeções e testes de aceite)

{T(['Fornecedor', 'Inspeções', 'Itens não conformes', 'Reprovadas', 'Custo de retrabalho (R$)'], [[fn.get(k, 'equipe própria'), g.n, f"{g.nc} de {g.it} ({pc(g.nc / g.it)})", g.rep, br(g.custo)] for k, g in q10.iterrows()])}

Defeitos da trilha ágil: {len(dfe)} (tabela 24). _(Marjorie: plano de qualidade — critérios de aceite, quem inspeciona, quando.)_
''')

# ------------------------------------------------------------ D11
alc = al.set_index('nivel_decisor')
def quem(m):
    for n in ['GERENTE', 'PATROCINADOR', 'COMITE']:
        if n not in alc.index: continue
        a = alc.loc[n]
        if (pd.isna(a.limite_custo_rs) or m.impacto_custo_rs <= a.limite_custo_rs) and (pd.isna(a.limite_prazo_du) or m.impacto_prazo_du <= a.limite_prazo_du) and (m.tipo_mudanca != 'ESCOPO' or a.pode_alterar_escopo == 'SIM'): return n
    return 'COMITE'
lin11 = [[m.id_mudanca, dt(m.data_abertura), m.id_solicitante, m.descricao, m.tipo_mudanca, br(m.impacto_custo_rs), m.impacto_prazo_du, m.impacto_pontos, m.status, m.nivel_decisor if isinstance(m.nivel_decisor, str) else '—', quem(m)] for m in sm.itertuples()]
dirs = bl[bl.origem == 'PEDIDO_DIRETO']
doc('D11', 'Mudanças e Bússola de Abordagem', 'Guilherme', 'tabelas 05, 14, 20 e 28 (com o boletim B8)', f'''
## 1. Registro de mudanças × matriz de alçadas

{T(['SM', 'Abertura', 'Solicitante', 'Descrição', 'Tipo', 'Custo (R$)', 'Prazo (du)', 'Pontos', 'Situação', 'Decidiu', 'Alçada exigida'], lin11)}

Alçadas (tabela 05): {'; '.join(f"{n}: até {rs(a.limite_custo_rs) if pd.notna(a.limite_custo_rs) else 'sem limite'} e {int(a.limite_prazo_du) if pd.notna(a.limite_prazo_du) else '∞'} du, escopo {a.pode_alterar_escopo}" for n, a in alc.iterrows())}.
**SM-014 (sistema de visão, R$ 264.200 e 10 du)** está em análise e passa da alçada do gerente: vai ao {quem(sm[sm.id_mudanca == 'SM-014'].iloc[0]) if (sm.id_mudanca == 'SM-014').any() else 'comitê'}.

## 2. Escopo que entrou sem controle

Itens PEDIDO_DIRETO (todos da engenharia da montadora, PI13): {', '.join(dirs.id_item)} + PA-195 (na S14) = **8 itens, 22 pontos**, sem solicitação de mudança. Custo estimado: 22 × custo real por ponto ({rs(C1['custoPonto'])}) = {rs(22 * C1['custoPonto'])}.

## 3. Bússola de Abordagem

| Domínio | Variável que decide | Preditiva quando… | Ágil quando… | No G7 |
|---|---|---|---|---|
| Escopo | estabilidade dos requisitos | o escopo é estável e contratado (equipamentos, obra) | o escopo é incerto e descoberto com o usuário (sistemas) | equipamentos e obra: preditiva; sistemas digitais: ágil |
| Mudança | custo de mudar depois | mudar é caro (concreto, máquina importada) | mudar é barato (software) | mudanças na linha passam pelo comitê; no software, pelo dono do produto, nunca direto |
| Entrega | entrega de uma vez × em partes | só tem valor completa (a linha) | entrega valor em partes (releases) | linha: uma entrega; sistemas: 3 releases |
| Usuário | proximidade do usuário | usuário distante, aceita no fim | usuário perto, revisa a cada sprint | operadores e engenharia da montadora nas revisões |

## 4. Mapa de interfaces entre as trilhas

| Ponto de encontro | Depende de | Prazo hoje | Quem responde |
|---|---|---|---|
| A47 teste de aceite em campo (SAT) | Release 2 (A58) | R2 prevista {dt(AG['releases']['R2']['data'])}; A47 começa em mar/2027 | gerente do projeto + dono do produto |
| A56 aceite final | Release 3 (A59) | R3 prevista {dt(AG['releases']['R3']['data'])} | gerente do projeto |
| Integração CLP × supervisório (A36/A37) | épico EP01 | _(completar)_ | integrador + time ágil |
''')

# ------------------------------------------------------------ D12
doc('D12', 'Estratégia do projeto', 'Caique', 'D4, D9, D11, D16; páginas Prazo e Cenários do sistema', f'''
## 1. Por que híbrido

A linha física (equipamentos importados, obra, elétrica, montagem) tem escopo contratado e mudança cara: é preditiva, com linha de base e controle por valor agregado. Os sistemas digitais têm requisitos que só aparecem com o uso: são ágeis, com backlog, sprints e releases. As duas trilhas se encontram no teste de aceite em campo (Release 2) e no aceite final (Release 3).

## 2. O que define o término hoje

A cadeia da **injetora importada**: {' → '.join(PV['cadeia'])}. O transporte e desembaraço (A12) está em 70% e atrasou 9 du; o término previsto é **{dt(PV['termino'])}**, {PV['du']} du além do contrato ({rs(PV['custoAtraso'])}).

## 3. Estratégia de prazo

- **Recuperar 1 du:** comprimir uma atividade crítica barata depois da A12 (ver D16/C2; a M4 mostra que só compensa comprimir dias que custam menos que R$ 50.100).
- **Proteger a Release 2:** bloquear pedidos diretos e manter a velocidade ≥ 16 pt/sprint, senão a R2 vira crítica.
- **Antecipar o benefício (C6):** produzir em um turno logo após os testes a frio, que é o cenário de maior resultado.

## 4. Governança e rotina de controle

Status semanal (avanço, horas, custos, quadro da sprint) → indicadores do sistema (término previsto, ENT, IDC/IDP, velocidade, exposição a riscos) → comitê mensal com decisão pedida. Alçadas: gerente até o limite da tabela 05; acima, patrocinador ou comitê.
''')

# ------------------------------------------------------------ D13
PS = S['pessoas']
lin13 = [[p['id_pessoa'], p['nome'], p['papel'], p['vinculo'], br(p['mensal'], 2), f"{p['custoHoraCalc']} {'✔' if p['confere'] else '✘'}", br(p['horas'], 1), br(p['custoHoras']), br(p['reajuste'])] for p in PS]
desv = [[f"{p['id_pessoa']} {p['nome']}", x['mes'], br(x['plan'], 1), br(x['apont'], 1), pc(x['pct'], 0)] for p in PS for x in p['desvios'] if x['pct'] is not None and abs(x['pct']) > 0.2]
doc('D13', 'Pessoal e custos de pessoal', 'Arley', 'tabelas 04, 18, 39 e 40; convenções 17 a 20; folha M8', f'''
## 1. Custo de cada pessoa (convenção 17)

{T(['Id', 'Nome', 'Papel', 'Vínculo', 'Custo mensal (R$)', 'R$/h (confere tab. 04)', 'Horas apontadas', 'Custo apontado (R$)', 'Reajuste até o fim (R$)'], lin13)}

Folha mensal: **{rs(sum(p['mensal'] for p in PS))}** (confere com o controle: R$ 282.910,40). Impacto total dos reajustes até {dt(PV['termino'])}: **{rs(sum(p['reajuste'] for p in PS))}** (convenção 19).

## 2. Planejado × apontado (desvio acima de 20%, convenção 18)

{T(['Pessoa', 'Mês', 'Planejado (h)', 'Apontado (h)', 'Desvio'], desv) if desv else 'Nenhum.'}

## 3. Trilha ágil: pontos por hora e custo por ponto (convenção 20)

{T(['Pessoa', 'Papel', 'Horas', 'Custo (R$)', 'Pontos concluídos', 'Pontos/hora', 'Custo/ponto (R$)'], [[f"{x['id']} {x['nome']}", x['papel'], br(x['horas'], 1), br(x['custo']), x['pontos'], br(x['ptsHora'], 3) if x['ptsHora'] else '—', br(x['custoPonto']) if x['custoPonto'] else '—'] for x in S['devs']])}

**Leitura:** _(Arley: quem está sobrecarregado, quem está abaixo do plano e o que fazer)_.
''')

# ------------------------------------------------------------ D14
PR = S['prod']
lin14 = [[p['id_atividade'], p['servico'], p['unidade'], br(p['quantidade_total'], 1), br(p['executado'], 1), p['hh'], br(p['real'], 3) if p['real'] else '—', br(p['produtividade_planejada'], 3), br(p['indProd'], 3) if p['indProd'] else '—', br(p['indEfetivo'], 3) if p['indEfetivo'] else '—', p['duracaoRestante'] if p['duracaoRestante'] is not None else '—', p['diagnostico']] for p in PR]
doc('D14', 'Produtividade das equipes', 'Arley', 'tabelas 41 e 42 (com o boletim B10); convenção 20; folha M8', f'''
## 1. Produtividade em 13/11/2026

{T(['Ativ.', 'Serviço', 'Un.', 'Total', 'Executado', 'Hh', 'Real (un/Hh)', 'Planejada', 'Índice de produtividade', 'Índice de efetivo', 'Duração restante (du)', 'Diagnóstico'], lin14)}

Fórmulas: real = quantidade ÷ Hh; índice de produtividade = real ÷ planejada; índice de efetivo = efetivo médio ÷ equipe planejada; duração restante = restante ÷ (real × efetivo das 3 últimas semanas × 8 h). Diagnóstico com índice abaixo de 0,9 (premissa do grupo).

## 2. Diagnóstico

- **A33 · elétrica:** produtividade e efetivo abaixo do plano ao mesmo tempo → falta gente **e** falta rendimento. Ação: cobrar do fornecedor (CT09) o efetivo contratado e um plano de recuperação; avaliar multa.
- **A39 · cabine de pintura:** produtividade acima do plano → concluída em 10/11.
- _(Arley: completar as demais)_
''')

# ------------------------------------------------------------ D15
a = C1['anos']
doc('D15', 'Análise financeira', 'José', 'tabela 02; convenções 6, 7, 16, 22 e 23; página Cenários', f'''
## 1. Estimativa no término (ENT)

ENT = ONT ÷ IDC = {rs(PJ['ont'])} ÷ {br(PJ['idc'], 3)} = **{rs(PJ['ent'])}** → desvio de **{rs(PJ['ent'] - PJ['ont'])}** ({pc(PJ['ent'] / PJ['ont'] - 1)}).

{T(['Entrega', 'ONT', 'CR', 'IDC', 'VC = VA − CR'], [[f"{e['entrega']} {nomeE.get(e['entrega'], '')}", br(e['ont']), br(e['cr']), br(e['idc'], 3) if e['idc'] else '—', br(e['vcusto'])] for e in EV['entregas']] + [['Frente ágil', br(EV['agil']['ont']), br(EV['agil']['cr']), br(EV['agil']['idc'], 3), br(EV['agil']['vcusto'])]])}

**De onde vem o desvio:** obra civil (1.3, IDC 0,83, sobre-medição do CT07), elétrica (1.4, IDC 0,85) e câmbio da injetora (CT03, R$ 812 mil, já dentro do CR da 1.2).

## 2. Fluxo de caixa e VPL hoje (cenário C1, convenção 23)

{T(['Ano', 'Benefício', 'Custo operacional', 'Investimento', 'Fluxo', 'Valor presente (14%)', 'Acumulado'], [[x['ano'], br(x['ben']), br(x['op']), br(x['inv']), br(x['fluxo']), br(x['fluxo'] / 1.14 ** x['ano']), br(x['acumulado'])] for x in a])}

- Ano 0 = 43.007.000 + (ENT − ONT); ano 1 reduzido em {br(C1['meses'], 2)} mês de atraso ÷ 12.
- **VPL {rs(C1['vpl'])}** (plano original: {rs(vpl0)}) · **payback {br(C1['payback'], 2)} anos** · custo do atraso {rs(C1['custoAtraso'])} ({PV['du']} du × R$ 50.100).

**Leitura:** o projeto continua com VPL positivo, mas cada R$ 1 de estouro sai direto do VPL do ano 0, e cada mês de atraso tira 1/12 do fluxo do primeiro ano (~R$ 510 mil). É a base para comparar os cenários (D16).
''')

# ------------------------------------------------------------ D16
lin16 = [[c['id'], c['nome'], dt(c['termino']), c['duAlemContrato'], br(c['ent']), br(c['vpl']), br(c['payback'], 2), br(c['custoAtraso']), f"**{br(c['resultado'])}**", br(c['resultado'] - C1['resultado'])] for c in S['cen']]
lin16b = [[' + '.join(c['ids']), dt(c['termino']), c['du'], br(c['ent']), br(c['vpl']), f"**{br(c['resultado'])}**", br(c['resultado'] - C1['resultado'])] for c in S['combos']]
doc('D16', 'Cenários e decisão', 'Diego', 'tabelas 02 e 43 a 46; convenções 21 a 23; página Cenários; folha M7', f'''
## 1. Os seis cenários (convenções 21 a 23)

{T(['Cenário', 'Nome', 'Término', 'du além', 'ENT (R$)', 'VPL (R$)', 'Payback', 'Custo do atraso', 'Resultado = VPL − atraso', 'vs. C1'], lin16)}

Conferência com o dossiê (M7): C1 10/05/2027 e ENT 41.764.252; C3 10/05/2027 e 41.389.882; C4 23/06/2027 e 42.969.789 ✔.

## 2. Combinações permitidas (coluna "combinável com" da tabela 43)

{T(['Combinação', 'Término', 'du além', 'ENT', 'VPL', 'Resultado', 'vs. C1'], lin16b)}

## 3. O que se perde em cada escolha

- **C2 recuperar o prazo:** termina antes do contrato, mas a compressão custa mais do que o atraso que evita.
- **C3 cortar escopo:** economiza custo, mas perde benefício (−1,4%) e eleva o custo operacional.
- **C4 ampliar o escopo:** maior VPL, mas 32 du de atraso (R$ 1,6 mi) derrubam o resultado.
- **C5 trocar a solução:** praticamente igual ao C1.
- **C6 dois estágios:** antecipa 60% do benefício (produção em um turno após os testes a frio) sem mexer no caminho crítico.

## 4. Recomendação ao comitê

**Aprovar o {MELHOR['id']} ({MELHOR['nome']})**: resultado de {rs(MELHOR['resultado'])}, {rs(MELHOR['resultado'] - C1['resultado'])} acima de seguir como está. Nenhuma combinação supera o {MELHOR['id']} sozinho.
**Decisão pedida:** aprovar o investimento adicional e a operação em um turno após os testes a frio · **dono:** gerente do projeto · **prazo:** comitê de dezembro/2026.
Em paralelo (sem custo): bloquear pedidos diretos (D11), cobrar multas (D10) e pedir o remanejamento da reserva gerencial (D9).
''')

# ------------------------------------------------------------ D17
dur = LB['ativ']
def ini(x):
    if x.vinculo_tipo != 'ATIVIDADE': return 999
    return min(dur[i]['ES'] for i in x.vinculo_ids.split(';') if i in dur)
els = el[el.vinculo_tipo != 'NENHUM'].copy(); els['ini'] = [ini(x) for x in els.itertuples()]; els = els.sort_values(['ini', 'id_elemento'])
doc('D17', 'Modelo 3D', 'Caique', 'tabela 38; página Modelo 3D do sistema (R12)', f'''
## 1. O modelo

24 elementos da tabela 38 (posição e volume em metros) desenhados no sistema com Three.js: terreno, galpão existente (envoltória transparente), Linha de painéis em operação, e os elementos novos. Cada elemento está ligado a atividades, a um épico ou às releases (campo `vinculo_ids`).

- **Controle de data:** até 13/11/2026 o avanço é o real (tabela 17); depois, a previsão pela rede.
- A altura e a cor sobem com o avanço; o vermelho marca o que está na cadeia do término e atrasado. Tocar num elemento mostra as atividades e o avanço de cada uma.

## 2. Etapas de implantação (ordem pela data de início da linha de base)

{T(['Etapa', 'Elemento', 'Nome', 'Ligado a', 'Início na linha de base'], [[k + 1, x.id_elemento, x.nome_elemento, x.vinculo_ids, dt(LB['ativ'][x.vinculo_ids.split(';')[0]]['inicio']) if x.ini < 999 else 'trilha ágil'] for k, x in enumerate(els.itertuples())])}

**Ordem de implantação proposta (campo `ordem_de_implantacao`):** a ordem acima. _(Caique: revisar e justificar; anexar 4 capturas da animação: projeto executivo, obra civil pronta, equipamentos montados e linha pronta.)_
''')

# ------------------------------------------------------------ gravar
FINAIS = {'D12','D1','D2','D3','D4','D5','D6','D9','D10','D13','D14','D16','D17'}  # lacunas preenchidas; não sobrescrever
CSS = '''@page { size: A4; margin: 13mm; } body { font-family: "DejaVu Sans", Arial, sans-serif; font-size: 10px; color: #1d2733; line-height: 1.4; }
h1 { font-size: 18px; color: #1f3a5f; border-bottom: 2px solid #1f3a5f; padding-bottom: 3px; } h2 { font-size: 13px; color: #1f3a5f; margin: 12px 0 4px; }
table { border-collapse: collapse; width: 100%; margin: 4px 0 8px; font-size: 8.8px; } th { background: #e8eef5; } th, td { border: 1px solid #c9d2dc; padding: 2px 4px; text-align: left; vertical-align: top; }
code { background: #f3f6f9; } em { color: #8a5a00; }'''
for cod, (tit, dono, md) in DOCS.items():
    if cod in FINAIS: continue  # versão revisada pelo responsável; não sobrescrever
    nome = f'{cod}_{tit.split(" (")[0].lower().replace(" ", "-").replace(",", "").replace("ç", "c").replace("ã", "a").replace("õ", "o").replace("é", "e").replace("ú", "u").replace("ó", "o").replace("á", "a").replace("í", "i").replace("ê", "e")}'
    open(f'{out}/{nome}.md', 'w').write(md)
    html = f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>{cod}</title><style>{CSS}</style></head><body>{markdown.markdown(md, extensions=["tables"])}</body></html>'
    open(f'{out}/{nome}.html', 'w').write(html)
    subprocess.run(['google-chrome', '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={out}/{nome}.pdf', f'{out}/{nome}.html'], capture_output=True)
    os.remove(f'{out}/{nome}.html'); print(cod, dono, nome)
