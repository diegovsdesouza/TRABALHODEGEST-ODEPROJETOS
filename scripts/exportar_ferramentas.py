"""Gera os arquivos de importação das ferramentas do enunciado a partir dos dados tratados.

Uso: python scripts/exportar_ferramentas.py dados/tratados docs
- docs/jira/backlog_jira.csv  · backlog em 30/10 (antes da S14) com épicos, pontos, prioridade e versões (D7)
- docs/projectlibre/cronograma_G7.xml · projeto no formato XML do MS Project, que o ProjectLibre abre (D4):
  calendário com feriados (tab. 11), EAP como tarefas-resumo (tab. 06), atividades com duração PERT (conv. 1)
  e predecessoras com tipo e defasagem (tab. 08, conv. 2)
- docs/projectlibre/avanco_13-11.csv · avanço real de cada atividade na data de status, para lançar depois da linha de base
"""
import os, sys, math, csv
import pandas as pd
from xml.sax.saxutils import escape as X

src, out = sys.argv[1], sys.argv[2]
r = lambda n: pd.read_csv(f'{src}/{n}.csv', dtype={'codigo_eap': str, 'codigo_pai': str})

# ---------------- Jira
os.makedirs(f'{out}/jira', exist_ok=True)
ep = r('13_epicos'); b = r('14_backlog_itens').sort_values('ordem_no_backlog')
TIPO = {'HISTORIA': 'Story', 'BUG': 'Bug', 'TECNICA': 'Task', 'SPIKE': 'Task'}
PRIO = {'MUST': 'Highest', 'SHOULD': 'High', 'COULD': 'Medium', 'WONT': 'Low'}
STAT = {'CONCLUIDO': 'Done', 'A_FAZER': 'To Do', 'EM_ANDAMENTO': 'In Progress', 'EM_TESTE': 'In Progress'}
idep = {e: i + 1 for i, e in enumerate(ep.id_epico)}
with open(f'{out}/jira/backlog_jira.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['Issue Id', 'Issue Type', 'Summary', 'Description', 'Story Points', 'Priority', 'Labels', 'Labels', 'Fix Version', 'Parent', 'Status'])
    for _, e in ep.iterrows():
        w.writerow([idep[e.id_epico], 'Epic', f'{e.id_epico} · {e.nome_epico}', f'Como {e.persona}, quero {e.beneficio_esperado}. Valor de negócio {e.valor_de_negocio}.', '', 'High', e.id_epico, '', e.id_release_planejada, '', 'To Do'])
    for k, x in enumerate(b.itertuples(), start=100):
        w.writerow([k, TIPO[x.tipo_item], f'{x.id_item} · {x.titulo}', x.historia_de_usuario if isinstance(x.historia_de_usuario, str) else '',
                    int(x.pontos), PRIO[x.prioridade_moscow], x.prioridade_moscow, x.origem, x.id_release, idep[x.id_epico], STAT[x.status]])

# ---------------- ProjectLibre (MSPDI)
os.makedirs(f'{out}/projectlibre', exist_ok=True)
eap = r('06_eap'); atv = r('07_atividades'); dep = r('08_dependencias'); cal = r('11_calendario')
dur = {x.id_atividade: int(x.duracao_fixa_du) if x.tipo_atividade == 'MARCO_AGIL' else math.ceil((x.duracao_otimista_du + 4 * x.duracao_mais_provavel_du + x.duracao_pessimista_du) / 6 - 1e-9)
       for x in atv.itertuples()}
feriados = cal[cal.feriado.notna() & (pd.to_datetime(cal.data).dt.dayofweek < 5)]
tarefas = []  # (uid, nome, nivel, resumo, id_atividade)
uid = 0
for e in eap[eap.nivel == 2].itertuples():
    uid += 1; tarefas.append((uid, f'{e.codigo_eap} {e.nome}', 1, True, None, e.codigo_eap))
    pacotes = eap[eap.codigo_pai == e.codigo_eap]
    for p in pacotes.itertuples():
        uid += 1; tarefas.append((uid, f'{p.codigo_eap} {p.nome}', 2, True, None, p.codigo_eap))
        for a in atv[atv.codigo_eap == p.codigo_eap].itertuples():
            uid += 1; tarefas.append((uid, f'{a.id_atividade} {a.nome_atividade}', 3, False, a.id_atividade, p.codigo_eap))
    for a in atv[atv.codigo_eap == e.codigo_eap].itertuples():  # atividades ligadas direto à entrega (marcos ágeis)
        uid += 1; tarefas.append((uid, f'{a.id_atividade} {a.nome_atividade}', 2, False, a.id_atividade, e.codigo_eap))
uid_de = {t[4]: t[0] for t in tarefas if t[4]}
faltam = set(atv.id_atividade) - set(uid_de)
assert not faltam, f'atividades fora da EAP: {faltam}'
preds = {}
for d in dep.itertuples():
    preds.setdefault(d.id_sucessora, []).append(d)

xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '<Project xmlns="http://schemas.microsoft.com/project">',
       '<Name>G7 Plásticos Abrantes · Linha de injeção e pintura</Name><Title>Linha de injeção e pintura de para-choques</Title>',
       '<ScheduleFromStart>1</ScheduleFromStart><StartDate>2026-02-02T08:00:00</StartDate><StatusDate>2026-11-13T17:00:00</StatusDate>',
       '<CalendarUID>1</CalendarUID><DefaultStartTime>08:00:00</DefaultStartTime><DefaultFinishTime>17:00:00</DefaultFinishTime>',
       '<MinutesPerDay>480</MinutesPerDay><MinutesPerWeek>2400</MinutesPerWeek><DaysPerMonth>20</DaysPerMonth><DurationFormat>7</DurationFormat>',
       '<Calendars><Calendar><UID>1</UID><Name>Projeto G7 (seg a sex, feriados da tabela 11)</Name><IsBaseCalendar>1</IsBaseCalendar><WeekDays>']
for dia in range(1, 8):
    if dia in (1, 7): xml.append(f'<WeekDay><DayType>{dia}</DayType><DayWorking>0</DayWorking></WeekDay>')
    else: xml.append(f'<WeekDay><DayType>{dia}</DayType><DayWorking>1</DayWorking><WorkingTimes><WorkingTime><FromTime>08:00:00</FromTime><ToTime>12:00:00</ToTime></WorkingTime><WorkingTime><FromTime>13:00:00</FromTime><ToTime>17:00:00</ToTime></WorkingTime></WorkingTimes></WeekDay>')
for f_ in feriados.itertuples():
    xml.append(f'<WeekDay><DayType>0</DayType><DayWorking>0</DayWorking><TimePeriod><FromDate>{f_.data}T00:00:00</FromDate><ToDate>{f_.data}T23:59:00</ToDate></TimePeriod></WeekDay>')
xml.append('</WeekDays></Calendar></Calendars><Tasks>')
xml.append('<Task><UID>0</UID><ID>0</ID><Name>Linha de injeção e pintura de para-choques</Name><OutlineLevel>0</OutlineLevel><Summary>1</Summary></Task>')
for i, (u, nome, nivel, resumo, ida, cod) in enumerate(tarefas, start=1):
    xml.append(f'<Task><UID>{u}</UID><ID>{i}</ID><Name>{X(nome)}</Name><OutlineLevel>{nivel}</OutlineLevel><WBS>{X(cod)}</WBS><Summary>{1 if resumo else 0}</Summary>')
    if not resumo:
        xml.append(f'<Duration>PT{dur[ida] * 8}H0M0S</Duration><DurationFormat>7</DurationFormat><Start>2026-02-02T08:00:00</Start><ConstraintType>0</ConstraintType><Manual>0</Manual>')
        for d in preds.get(ida, []):
            tipo = 1 if d.tipo_dependencia == 'TI' else 3  # 1 = FS (término-início), 3 = SS (início-início)
            xml.append(f'<PredecessorLink><PredecessorUID>{uid_de[d.id_predecessora]}</PredecessorUID><Type>{tipo}</Type><LinkLag>{int(d.defasagem_du) * 4800}</LinkLag><LagFormat>7</LagFormat></PredecessorLink>')
    xml.append('</Task>')
xml.append('</Tasks></Project>')
open(f'{out}/projectlibre/cronograma_G7.xml', 'w', encoding='utf-8').write('\n'.join(xml))

# avanço real na data de status (histórico tratado + boletim B1)
av = r('17_avanco_semanal')
b1 = pd.DataFrame([dict(semana_fim='2026-11-13', id_atividade='A12', avanco_acumulado_pct=70, situacao='EM_ANDAMENTO', data_inicio_real='2026-10-20'),
                   dict(semana_fim='2026-11-13', id_atividade='A33', avanco_acumulado_pct=90, situacao='EM_ANDAMENTO', data_inicio_real='2026-09-14'),
                   dict(semana_fim='2026-11-13', id_atividade='A35', avanco_acumulado_pct=100, situacao='CONCLUIDA', data_inicio_real='2026-09-29', data_termino_real='2026-11-09'),
                   dict(semana_fim='2026-11-13', id_atividade='A39', avanco_acumulado_pct=100, situacao='CONCLUIDA', data_inicio_real='2026-10-07', data_termino_real='2026-11-10')])
u = pd.concat([av, b1]).sort_values('semana_fim').groupby('id_atividade').tail(1)
rel = {'A57': ('2026-05-04', '2026-08-07', 100)}
linhas = [dict(atividade=a.id_atividade, nome=atv.set_index('id_atividade').nome_atividade[a.id_atividade], percentual=int(a.avanco_acumulado_pct),
               inicio_real=a.data_inicio_real, termino_real=a.data_termino_real if isinstance(a.data_termino_real, str) else '') for a in u.itertuples()]
linhas += [dict(atividade=k, nome=atv.set_index('id_atividade').nome_atividade[k], percentual=v[2], inicio_real=v[0], termino_real=v[1]) for k, v in rel.items()]
pd.DataFrame(linhas).sort_values('atividade').to_csv(f'{out}/projectlibre/avanco_13-11.csv', index=False)
print('ok', len(b), 'itens Jira ·', len(tarefas), 'linhas no cronograma ·', len(linhas), 'atividades com avanço')
