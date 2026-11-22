"""Tratamento dos dados do G7 Plásticos Abrantes (ENGN62, UFBA 2026.2).

Uso:  python scripts/tratamento_dados.py dados/brutos dados/tratados docs/log_tratamento.csv
Lê as 46 tabelas brutas, aplica as regras Q1 a Q6, grava as tratadas e o log linha a linha,
e confere o resultado com os números de controle do dossiê (histórico até 30/10/2026).
"""
import sys, os, glob, shutil
import pandas as pd

src, dst, logp = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(dst, exist_ok=True)
log = []
def L(tab, chave, campo, antes, depois, regra):
    log.append(dict(tabela=tab, chave=chave, campo=campo, valor_original=antes, valor_novo=depois, regra=regra))
r = lambda n: pd.read_csv(f"{src}/{n}.csv")
T = {os.path.basename(f)[:-4]: pd.read_csv(f) for f in sorted(glob.glob(f"{src}/*.csv"))}

# Q1 — 18_apontamento_horas: duplicatas exatas
h = T["18_apontamento_horas"]
dup = h[h.duplicated()]
for _, x in dup.iterrows():
    L("18_apontamento_horas", f"{x.semana_inicio}|{x.id_pessoa}|{x.id_item}", "linha inteira",
      f"HN={x.horas_normais}; HE={x.horas_extras}", "REMOVIDA", "Q1 duplicata exata")
h = h.drop_duplicates().copy()

# Q2 — 18_apontamento_horas: casa decimal deslocada (valor 10x maior que a semana da pessoa)
for (sem, pes, item), novo in {("2026-03-16", "P02", "GESTAO"): 40.0,
                               ("2026-10-05", "P17", "S12"): 20.0,
                               ("2026-08-17", "P08", "A29"): 17.0}.items():
    m = (h.semana_inicio == sem) & (h.id_pessoa == pes) & (h.id_item == item)
    L("18_apontamento_horas", f"{sem}|{pes}|{item}", "horas_normais", h.loc[m, "horas_normais"].iloc[0], novo,
      "Q2 casa decimal (10x); total confere com o controle de 11.708,5 h")
    h.loc[m, "horas_normais"] = novo
T["18_apontamento_horas"] = h

# Q3 — 19_custos_realizados: lançamentos DIVERSOS, sem atividade -> reapropriar pelo documento
c = T["19_custos_realizados"].copy(); a = T["07_atividades"]; med = T["31_contratos_medicoes"]
for i in c.index[c.codigo_eap == "DIVERSOS"]:
    doc = c.at[i, "documento"]
    if doc.startswith("MED-"):
        ativ = med.loc[med.id_medicao == doc, "id_atividade"].iloc[0]; ev = f"medição {doc} na tabela 31"
    else:  # NF-Axx-nnn
        ativ = doc.split("-")[1]; ev = f"código da atividade no documento {doc}"
    eap = a.loc[a.id_atividade == ativ, "codigo_eap"].iloc[0]
    L("19_custos_realizados", c.at[i, "id_lancamento"], "id_atividade; codigo_eap", "vazio; DIVERSOS",
      f"{ativ}; {eap}", f"Q3 reapropriado por evidência: {ev}")
    c.at[i, "id_atividade"], c.at[i, "codigo_eap"] = ativ, eap
T["19_custos_realizados"] = c

# Q4 — 17_avanco_semanal: semanas sem informe dentro do período da atividade -> repetir o último valor
av = T["17_avanco_semanal"].copy(); av["sf"] = pd.to_datetime(av.semana_fim); novas = []
for k, g in av.groupby("id_atividade"):
    g = g.sort_values("sf")
    for d in pd.date_range(g.sf.min(), g.sf.max(), freq="7D"):
        if d not in set(g.sf):
            ant = g[g.sf < d].iloc[-1].copy(); ant["semana_fim"] = d.date().isoformat(); ant["sf"] = d
            novas.append(ant)
            L("17_avanco_semanal", f"{ant.semana_fim}|{k}", "linha inteira", "AUSENTE",
              f"avanço {ant.avanco_acumulado_pct}% (repetido)", "Q4 semana faltante preenchida com o último informe")
av = pd.concat([av, pd.DataFrame(novas)]).sort_values(["semana_fim", "id_atividade"]).drop(columns="sf")
T["17_avanco_semanal"] = av

# Q5 — 21_itens_transicoes: status digitado fora do padrão
t = T["21_itens_transicoes"].copy()
norm = t.status_destino.str.strip().str.upper().str.replace(" ", "_").replace({"DONE": "CONCLUIDO"})
for i in t.index[norm != t.status_destino]:
    L("21_itens_transicoes", t.at[i, "id_transicao"], "status_destino", t.at[i, "status_destino"], norm[i],
      "Q5 status padronizado no domínio do dicionário")
t["status_destino"] = norm; T["21_itens_transicoes"] = t

# Q6 — 25_inspecoes_aceite: resultado digitado fora do padrão
ins = T["25_inspecoes_aceite"].copy(); n2 = ins.resultado.str.strip().str.upper()
for i in ins.index[n2 != ins.resultado]:
    L("25_inspecoes_aceite", ins.at[i, "id_inspecao"], "resultado", ins.at[i, "resultado"], n2[i],
      "Q6 resultado padronizado no domínio do dicionário")
ins["resultado"] = n2; T["25_inspecoes_aceite"] = ins

for n, df in T.items():
    df.to_csv(f"{dst}/{n}.csv", index=False)
pd.DataFrame(log).to_csv(logp, index=False)

# Conferência com os números de controle (histórico até 30/10/2026)
h, c, b = T["18_apontamento_horas"], T["19_custos_realizados"], T["14_backlog_itens"]
ctrl = [
    ("Horas apontadas (normais + extras), tab. 18", 11708.5, (h.horas_normais + h.horas_extras).sum()),
    ("Linhas de apontamento, tab. 18", 508, len(h)),
    ("Custos lançados (R$), tab. 19", 35573360.67, c.valor_rs.sum()),
    ("Custos da frente preditiva (R$), tab. 19", 34632983.98, c[c.frente == "PREDITIVA"].valor_rs.sum()),
    ("Lançamentos de custo, tab. 19", 142, len(c)),
    ("Itens no backlog, tab. 14", 94, len(b)),
    ("Itens concluídos, tab. 14", 65, (b.status == "CONCLUIDO").sum()),
    ("Pontos concluídos, tab. 14", 209, b[b.status == "CONCLUIDO"].pontos.sum()),
    ("Transições de status, tab. 21", 297, len(T["21_itens_transicoes"])),
    ("Informes de avanço, tab. 17", 259, len(T["17_avanco_semanal"])),
    ("Homens-hora das equipes, tab. 42", 15860, T["42_producao_semanal"].hh_trabalhadas.sum()),
    ("Linhas de produção semanal, tab. 42", 57, len(T["42_producao_semanal"])),
]
s = T["39_cargos_salarios"]
ctrl.append(("Custo mensal da folha (R$), tab. 39", 282910.40,
             (s.remuneracao_mensal_rs * (1 + s.encargos_pct / 100) + s.beneficios_mensais_rs).sum()))
print(f"{len(log)} alterações registradas em {logp}\n")
for nome, esp, obt in ctrl:
    print(f"{'OK ' if abs(esp - obt) < 0.01 else 'XX '} {nome}: esperado {esp:,.2f} | obtido {obt:,.2f}")
