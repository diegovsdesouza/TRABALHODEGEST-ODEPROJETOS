"""Gera os scripts SQL do Supabase (tabelas, regras de acesso e carga do histórico tratado) a partir de dados/tratados.

Uso: python scripts/build_supabase.py dados/tratados supabase
Cada CSV vira uma tabela com o nome sem o número (ex.: 17_avanco_semanal -> avanco_semanal).
Toda tabela ganha: id (chave), fonte_registro (HISTORICO ou TELA), lancado_por_email e lancado_em,
para provar quem lançou cada boletim (exigência de pelo menos três integrantes).
"""
import os, re, sys, glob
import pandas as pd

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
TEXTO = {"codigo_eap", "codigo_pai", "valor", "versao", "vinculo_ids", "predecessoras", "sucessoras", "combinavel_com"}
RI, RF, RD = re.compile(r"^-?\d+$"), re.compile(r"^-?\d+(\.\d+)?$"), re.compile(r"^\d{4}-\d{2}-\d{2}$")

def tipo(col, s):
    v = s.dropna()
    if col in TEXTO or not len(v): return "text"
    if v.map(lambda x: bool(RD.match(x))).all(): return "date"
    if v.map(lambda x: bool(RI.match(x))).all(): return "integer"
    if v.map(lambda x: bool(RF.match(x))).all(): return "numeric"
    return "text"

def lit(v, t):
    if pd.isna(v) or v == "": return "null"
    if t in ("integer", "numeric"): return v
    return "'" + str(v).replace("'", "''") + "'"

def nome(f):
    return os.path.basename(f)[:-4].split("_", 1)[1]

schema = ["-- 01_schema.sql · G7 Plásticos Abrantes · gerado por scripts/build_supabase.py",
          "-- SQL Editor → New query → colar → Run. Pode rodar de novo: apaga e recria tudo.", ""]
cargas = {"02": [], "03": [], "04": []}
tabs = []
for f in sorted(glob.glob(f"{src}/*.csv")):
    num, tab = int(os.path.basename(f)[:2]), nome(f)
    df = pd.read_csv(f, dtype=str, keep_default_na=False).replace("", pd.NA)
    tipos = {c: tipo(c, df[c]) for c in df.columns}
    defs = ["  id bigserial primary key"] + [f"  {c} {t}" for c, t in tipos.items()] + [
        "  fonte_registro text not null default 'TELA'",
        "  lancado_por_email text default (auth.jwt() ->> 'email')",
        "  lancado_em timestamptz not null default now()"]
    schema += [f"drop table if exists public.{tab} cascade;", f"create table public.{tab} (\n" + ",\n".join(defs) + "\n);"]
    tabs.append(tab)
    cols = list(df.columns)
    linhas = ["(" + ",".join([lit(v, tipos[c]) for c, v in zip(cols, r)] + ["'HISTORICO'"]) + ")" for r in df.itertuples(index=False)]
    bloco = "02" if num <= 16 else ("03" if num <= 37 else "04")
    for i in range(0, len(linhas), 300):
        cargas[bloco].append(f"insert into public.{tab} ({','.join(cols)},fonte_registro) values\n" + ",\n".join(linhas[i:i + 300]) + ";")

schema += ["", "-- Regras de acesso (RLS): qualquer um lê; só integrante logado lança, edita ou apaga"]
for t in tabs:
    schema += [f"alter table public.{t} enable row level security;",
               f'create policy "{t}_leitura" on public.{t} for select to anon, authenticated using (true);',
               f'create policy "{t}_escrita" on public.{t} for all to authenticated using (true) with check (true);']
schema += ["", "grant usage on schema public to anon, authenticated;",
           "grant select on all tables in schema public to anon, authenticated;",
           "grant insert, update, delete on all tables in schema public to authenticated;",
           "grant usage, select on all sequences in schema public to authenticated;"]
open(f"{out}/01_schema.sql", "w").write("\n".join(schema) + "\n")
desc = {"02": "Blocos A a C (governança, plano preditivo e plano ágil)", "03": "Bloco D (execução e controle, histórico até 30/10)",
        "04": "Blocos E a G (modelo 3D, pessoas e cenários)"}
nomes = {"02": "02_carga_planejamento.sql", "03": "03_carga_execucao.sql", "04": "04_carga_pessoas_cenarios.sql"}
for k, partes in cargas.items():
    head = [f"-- {nomes[k]} · {desc[k]} · dados TRATADOS (dados/tratados). Rode depois do 01_schema.sql.",
            "-- A quinzena de campo (03 a 13/11) NÃO está aqui: ela é lançada pelas telas do sistema.", "begin;"]
    open(f"{out}/{nomes[k]}", "w").write("\n".join(head + partes + ["commit;"]) + "\n")
for n in sorted(os.listdir(out)):
    print(n, os.path.getsize(f"{out}/{n}") // 1024, "KB")
