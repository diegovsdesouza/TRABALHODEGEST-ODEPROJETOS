"""Rede da linha de base (convenções 1 e 2) — G7 Plásticos Abrantes.

Uso: python scripts/cpm.py dados/tratados docs/linha_de_base.csv
Duração: ESTIMADA = ceil((O + 4M + P) / 6); MARCO_AGIL = duracao_fixa_du.
TI: início ≥ término da predecessora + 1 + defasagem.  II: início ≥ início da predecessora + defasagem.
Dia útil 1 = data_inicio_projeto (tabela 11, dia_util_projeto). Linha de base nas datas mais cedo.
"""
import sys, math
import pandas as pd

def duracoes(a):
    d = {}
    for _, x in a.iterrows():
        if x.tipo_atividade == "MARCO_AGIL":
            d[x.id_atividade] = int(x.duracao_fixa_du)
        else:
            d[x.id_atividade] = math.ceil((x.duracao_otimista_du + 4 * x.duracao_mais_provavel_du + x.duracao_pessimista_du) / 6 - 1e-9)
    return d

def cpm(ids, dur, dep):
    """ids em qualquer ordem; dep: lista de (pred, suc, tipo, lag). Retorna dict com ES, EF, LS, LF, folga."""
    preds = {i: [] for i in ids}; sucs = {i: [] for i in ids}
    for p, s, t, l in dep:
        preds[s].append((p, t, l)); sucs[p].append((s, t, l))
    # ordem topológica
    ordem, grau = [], {i: len(preds[i]) for i in ids}
    fila = [i for i in ids if grau[i] == 0]
    while fila:
        i = fila.pop(0); ordem.append(i)
        for s, _, _ in sucs[i]:
            grau[s] -= 1
            if grau[s] == 0: fila.append(s)
    assert len(ordem) == len(ids), "a rede tem ciclo"
    ES, EF = {}, {}
    for i in ordem:
        es = 1
        for p, t, l in preds[i]:
            es = max(es, EF[p] + 1 + l if t == "TI" else ES[p] + l)
        ES[i] = es; EF[i] = es + dur[i] - 1
    fim = max(EF.values())
    LS, LF = {}, {}
    for i in reversed(ordem):
        lf = fim
        for s, t, l in sucs[i]:
            lf = min(lf, LS[s] - 1 - l if t == "TI" else LS[s] - l + dur[i] - 1)
        LF[i] = lf; LS[i] = lf - dur[i] + 1
    return {i: dict(ES=ES[i], EF=EF[i], LS=LS[i], LF=LF[i], folga=LS[i] - ES[i]) for i in ids}, fim

if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    a = pd.read_csv(f"{src}/07_atividades.csv"); d = pd.read_csv(f"{src}/08_dependencias.csv")
    cal = pd.read_csv(f"{src}/11_calendario.csv").dropna(subset=["dia_util_projeto"])
    du2data = dict(zip(cal.dia_util_projeto.astype(int), cal.data))
    dur = duracoes(a)
    res, fim = cpm(list(a.id_atividade), dur, list(d.itertuples(index=False, name=None)))
    df = pd.DataFrame.from_dict(res, orient="index").reset_index(names="id_atividade")
    df = a[["id_atividade", "codigo_eap", "nome_atividade", "disciplina", "tipo_atividade"]].merge(df)
    df.insert(5, "duracao_du", df.id_atividade.map(dur))
    df["critica"] = (df.folga == 0).astype(int)
    df["inicio_lb"] = df.ES.map(du2data); df["termino_lb"] = df.EF.map(du2data)
    df.to_csv(out, index=False)
    print(f"Término da linha de base: du {fim} = {du2data[fim]}")
    print("Caminho crítico:", " → ".join(df[df.critica == 1].sort_values("ES").id_atividade))
