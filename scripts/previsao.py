"""Previsão de término na data de status (convenções 8, 10 e 11) — G7 Plásticos Abrantes.

Uso: python scripts/previsao.py dados/tratados docs/linha_de_base.csv
Aplica os boletins B1 (avanço) e B5/B6 (sprint S14) do dossiê sobre o histórico até 30/10
e calcula: velocidade média, previsão das releases R2 e R3 e o término previsto pela rede.
"""
import sys, math
import pandas as pd

src, lbp = sys.argv[1], sys.argv[2]
STATUS = "2026-11-13"
a = pd.read_csv(f"{src}/07_atividades.csv"); dep = pd.read_csv(f"{src}/08_dependencias.csv")
cal = pd.read_csv(f"{src}/11_calendario.csv")
lb = pd.read_csv(lbp).set_index("id_atividade")
uteis = cal.dropna(subset=["dia_util_projeto"])
d2du = dict(zip(uteis.data, uteis.dia_util_projeto.astype(int))); du2d = {v: k for k, v in d2du.items()}
st = d2du[STATUS]

# --- trilha ágil: backlog atualizado com a sprint S14 (boletins B5 e B6)
b = pd.read_csv(f"{src}/14_backlog_itens.csv")
b = pd.concat([b, pd.DataFrame([
    dict(id_item="PA-195", pontos=2, prioridade_moscow="SHOULD", id_release="R2", origem="PEDIDO_DIRETO", status="A_FAZER"),
    dict(id_item="PA-196", pontos=2, prioridade_moscow="MUST", id_release="R2", origem="DEFEITO", status="A_FAZER")])])
concl_s14 = ["PA-140", "PA-185", "PA-188", "PA-192", "PA-195", "PA-190", "PA-186", "PA-194"]
b.loc[b.id_item.isin(concl_s14), "status"] = "CONCLUIDO"
si = pd.read_csv(f"{src}/20_sprint_itens.csv")
vel = si[si.concluido_na_sprint == 1].groupby("id_sprint").pontos.sum().to_dict()
vel["S14"] = int(b[b.id_item.isin(concl_s14)].pontos.sum())
ult5 = [f"S{n:02d}" for n in range(10, 15)]
vmed = sum(vel[s] for s in ult5) / 5
print(f"Itens concluídos: {(b.status == 'CONCLUIDO').sum()} · pontos concluídos: {b[b.status == 'CONCLUIDO'].pontos.sum()} (controle: 73 e 224)")
print("Velocidade S10–S14:", [vel[s] for s in ult5], f"→ média {vmed:.1f} pontos/sprint")
fim_sprint = cal.dropna(subset=["id_sprint"]).groupby("id_sprint").data.max().to_dict()
prev_rel = {}
for j, rel in enumerate(["R1", "R2", "R3"], 1):
    rest = b[(b.status != "CONCLUIDO") & (b.prioridade_moscow != "WONT") & (b.id_release.isin([f"R{k}" for k in range(1, j + 1)]))].pontos.sum()
    n = math.ceil(rest / vmed) if rest else 0
    sp = f"S{14 + n:02d}"
    prev_rel[rel] = fim_sprint.get(sp) if n else None
    print(f"  {rel}: {rest} pontos restantes → {n} sprints → fim da {sp} = {prev_rel[rel]}")

# --- trilha preditiva: último avanço com o boletim B1
av = pd.read_csv(f"{src}/17_avanco_semanal.csv")
av = pd.concat([av, pd.DataFrame([
    dict(semana_fim="2026-11-13", id_atividade="A12", avanco_acumulado_pct=70, situacao="EM_ANDAMENTO", data_inicio_real="2026-10-20"),
    dict(semana_fim="2026-11-13", id_atividade="A33", avanco_acumulado_pct=90, situacao="EM_ANDAMENTO", data_inicio_real="2026-09-14"),
    dict(semana_fim="2026-11-13", id_atividade="A35", avanco_acumulado_pct=100, situacao="CONCLUIDA", data_inicio_real="2026-09-29", data_termino_real="2026-11-09"),
    dict(semana_fim="2026-11-13", id_atividade="A39", avanco_acumulado_pct=100, situacao="CONCLUIDA", data_inicio_real="2026-10-07", data_termino_real="2026-11-10")])])
ult = av.sort_values("semana_fim").groupby("id_atividade").tail(1).set_index("id_atividade")

def du(data):  # data real -> dia útil (se cair em dia não útil, usa o útil anterior)
    while data not in d2du:
        data = (pd.Timestamp(data) - pd.Timedelta(days=1)).date().isoformat()
    return d2du[data]

preds = {i: [] for i in a.id_atividade}
for p, s, t, l in dep.itertuples(index=False, name=None):
    preds[s].append((p, t, l))
ES, EF, sit = {}, {}, {}
pend = list(a.id_atividade)
while pend:
    for i in list(pend):
        if any(p in pend for p, _, _ in preds[i]):
            continue
        tipo = a.loc[a.id_atividade == i, "tipo_atividade"].iloc[0]
        if i in ult.index and ult.loc[i, "situacao"] == "CONCLUIDA":
            ES[i], EF[i], sit[i] = du(ult.loc[i, "data_inicio_real"]), du(ult.loc[i, "data_termino_real"]), "CONCLUIDA"
        elif tipo == "MARCO_AGIL" and i == "A57":  # Release 1 implantada em 07/08/2026
            ES[i], EF[i], sit[i] = int(lb.loc[i, "ES"]), d2du["2026-08-07"], "CONCLUIDA"
        elif tipo == "MARCO_AGIL":
            rel = {"A58": "R2", "A59": "R3"}[i]
            es = max([1] + [EF[p] + 1 + l if t == "TI" else ES[p] + l for p, t, l in preds[i]])
            ES[i], EF[i], sit[i] = es, max(es, d2du[prev_rel[rel]]), "PREVISTA_PELA_RELEASE"
        elif i in ult.index:
            ES[i] = du(ult.loc[i, "data_inicio_real"])
            EF[i] = st + math.ceil(lb.loc[i, "duracao_du"] * (1 - ult.loc[i, "avanco_acumulado_pct"] / 100) - 1e-9)
            sit[i] = "EM_ANDAMENTO"
        else:
            es = max([st + 1] + [EF[p] + 1 + l if t == "TI" else ES[p] + l for p, t, l in preds[i]])
            ES[i], EF[i], sit[i] = es, es + int(lb.loc[i, "duracao_du"]) - 1, "NAO_INICIADA"
        pend.remove(i)

fim = max(EF.values()); contrato = d2du["2027-05-07"]
print(f"\nTérmino previsto: du {fim} = {du2d[fim]} · linha de base {du2d[int(lb.EF.max())]} · contrato 07/05/2027")
print(f"Dias úteis além do contrato: {fim - contrato} · custo do atraso: R$ {max(0, fim - contrato) * 50100:,.0f}")
# cadeia que define a data: volta pelas predecessoras que amarram
cad, i = [], max(EF, key=EF.get)
while True:
    cad.append(i)
    amarra = [p for p, t, l in preds[i] if (EF[p] + 1 + l if t == "TI" else ES[p] + l) == ES[i]]
    if not amarra or sit[i] == "CONCLUIDA":
        break
    i = amarra[0]
print("Cadeia que define o término:", " ← ".join(cad))
out = pd.DataFrame(dict(id_atividade=list(EF), situacao=[sit[i] for i in EF], inicio_du=[ES[i] for i in EF],
                        termino_du=list(EF.values()), termino_previsto=[du2d[EF[i]] for i in EF]))
out["termino_lb"] = out.id_atividade.map(lb.termino_lb)
out["desvio_du"] = out.termino_du - out.id_atividade.map(lb.EF)
out["na_cadeia_do_termino"] = out.id_atividade.isin(cad).astype(int)
out.sort_values("inicio_du").to_csv("docs/previsao_status.csv", index=False)
