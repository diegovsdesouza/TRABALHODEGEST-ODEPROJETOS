"""Roteiro de lançamento individual, passo a passo (um PDF por integrante).

Uso: python scripts/roteiro_individual.py dados/tratados docs/lancamento
Cada linha de boletim vira um cartão: em que aba tocar, o que escolher ou digitar em cada campo (com o texto
exatamente como aparece na tela) e quando salvar. Dados: testes/boletins_dados.py (os mesmos do teste automático).
"""
import os, re, sys, html, subprocess
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'testes'))
import roteiro_lancamento as R
from boletins_dados import B, MOV

src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
E = html.escape
rd = lambda n: pd.read_csv(f'{src}/{n}.csv', dtype=str).fillna('')
atv, eq, ct, fo, pi, sp, bl, epi, okr = (rd(n) for n in ['07_atividades', '04_equipe', '30_contratos', '29_fornecedores', '03_partes_interessadas', '15_sprints', '14_backlog_itens', '13_epicos', '36_okr_medicoes'])
dt = lambda v: '/'.join(reversed(v.split('-'))) if re.fullmatch(r'\d{4}-\d{2}-\d{2}', v) else v
itens = dict(zip(bl.id_item, bl.titulo)); itens.update({'PA-195': 'Gerar um relatório extra para a reunião de produção', 'PA-196': 'Corrigir a falha em: Configurar o monitoramento e os registros: Rastreabilidade de lotes e qualidade'})
ROTULO = {
    'atividades': {r.id_atividade: f'{r.id_atividade} · {r.nome_atividade}' for r in atv.itertuples()},
    'pessoas': {r.id_pessoa: f'{r.id_pessoa} · {r.nome} ({r.papel})' for r in eq.itertuples()},
    'dev': {r.id_pessoa: f'{r.id_pessoa} · {r.nome}' for r in eq.itertuples()},
    'contratos': {r.id_contrato: f'{r.id_contrato} · {r.objeto}' for r in ct.itertuples()},
    'fornecedores': {r.id_fornecedor: f'{r.id_fornecedor} · {r.nome}' for r in fo.itertuples()},
    'partes': {r.id_parte: f'{r.id_parte} · {r.parte_interessada}' for r in pi.itertuples()},
    'sprints': {r.id_sprint: f'{r.id_sprint} · {dt(r.data_inicio)} a {dt(r.data_fim)}' for r in sp.itertuples()},
    'itens': {k: f'{k} · {v[:60]}' for k, v in itens.items()},
    'epicos': {r.id_epico: f'{r.id_epico} · {r.nome_epico}' for r in epi.itertuples()},
    'krs': {r.id_resultado_chave: f'{r.id_resultado_chave} · {r.resultado_chave}' for r in okr.itertuples()},
    'medicoesPendentes': {},
}
FIXO = {'situacao': {'EM_ANDAMENTO': 'Em andamento', 'CONCLUIDA': 'Concluída'}, 'falhou': {'0': 'não', '1': 'sim'},
        'patrocinador_presente': {'0': 'não', '1': 'sim'}, 'ata_publicada': {'0': 'não', '1': 'sim'}}

# campos de cada tela, na ordem da tela: (campo, rótulo, tipo, nome da lista)
telas_js = open(os.path.join(os.path.dirname(__file__), '..', 'app', 'js', 'telas.js')).read()
CAMPOS = {k: [(c, rot, tp, (re.search(r"op: '(\w+)'", resto) or [None, None])[1]) for c, rot, tp, resto in re.findall(r"\['(\w+)', '([^']+)', '(data|int|num|txt|sel)'(.*?)\]", v)]
          for k, v in R.BLOCOS.items()}

def passo_campo(campo, rot, tp, op, valor):
    if valor is None or valor == '':
        return f'<li><b>{E(rot)}</b>: deixe <i>vazio</i>' + (' (escolha "— vazio —")' if tp == 'sel' else '') + '</li>'
    if tp == 'sel':
        txt = FIXO.get(campo, {}).get(valor) or ROTULO.get(op, {}).get(valor) or valor
        return f'<li><b>{E(rot)}</b>: toque e escolha <span class="v">{E(txt)}</span></li>'
    if tp == 'data':
        return f'<li><b>{E(rot)}</b>: escolha a data <span class="v">{dt(valor)}</span></li>'
    v = valor.replace('.', ',') if tp == 'num' else valor
    return f'<li><b>{E(rot)}</b>: digite <span class="v">{E(v)}</span></li>'

def cartoes(tela, linhas, comp=''):
    titulo = R.TIT[tela]; bol = R.BOL[tela]
    h = [f'<h2><span class="chip">{bol}</span> {E(titulo)}{" · " + comp if comp else ""} <small>({len(linhas)} linha{"s" if len(linhas) > 1 else ""})</small></h2>',
         f'<p class="abrir">Em <b>Lançamentos</b>, toque no botão <span class="v">{bol} {E(titulo)}</span>.</p>']
    if tela in R.AVISO: h.append(f'<p class="dica">⚠️ {R.AVISO[tela]}</p>')
    for i, l in enumerate(linhas, 1):
        passos = ''.join(passo_campo(c, rot, tp, op, l.get(c)) for c, rot, tp, op in CAMPOS[tela])
        h.append(f'<div class="card"><div class="n">Linha {i} de {len(linhas)}</div><ol>{passos}<li><b>Toque em Salvar</b> e espere aparecer "Salvo em …" embaixo da tela. ☐</li></ol></div>')
    return ''.join(h)

def quadro():
    h = ['<h2><span class="chip">B6</span> Quadro da sprint <small>(32 movimentos)</small></h2>',
         '<p class="abrir">Em <b>Lançamentos</b>, toque em <span class="v">B6 Quadro da sprint (mover cartões)</span>. No topo, em <b>Sprint</b>, confira que está <span class="v">S14 · 02/11/2026 a 13/11/2026</span>. Os cartões aparecem em 5 colunas: A FAZER, EM ANDAMENTO, EM REVISAO, EM TESTE e CONCLUIDO.</p>',
         '<p class="dica">⚠️ Cada movimento tem 3 ajustes no topo (data, quem moveu e, só para EM REVISAO, revisão por par) e depois a escolha da coluna <b>no próprio cartão</b>. O cartão muda de coluna sozinho: não precisa tocar em Salvar. Faça na ordem exata, um por vez.</p>']
    nomes = ROTULO['dev']
    for i, (d, it, para, q, rev) in enumerate(MOV, 1):
        r = f'<li>Em <b>Revisão por par</b>, escolha <span class="v">{"sim" if rev == "1" else "não"}</span></li>' if rev is not None else ''
        h.append(f'<div class="card"><div class="n">Movimento {i} de {len(MOV)}</div><ol><li>Em <b>Data do movimento</b>, escolha <span class="v">{dt(d)}</span></li>'
                 f'<li>Em <b>Quem moveu</b>, escolha <span class="v">{E(nomes[q])}</span></li>{r}'
                 f'<li>Ache o cartão <span class="v">{it}</span> e, na listinha dentro dele, escolha <span class="v">{para}</span></li>'
                 f'<li>Confira que o cartão {it} foi para a coluna <b>{para.replace("_", " ")}</b>. ☐</li></ol></div>')
    return ''.join(h)

CSS = '''@page { size: A4; margin: 12mm; } body { font-family: "DejaVu Sans", Arial, sans-serif; font-size: 11px; color: #1d2733; line-height: 1.45; }
h1 { font-size: 20px; color: #1f3a5f; margin: 0; } .sub { color: #6b7785; margin: 2px 0 8px; } h2 { font-size: 14px; color: #fff; background: #1f3a5f; padding: 5px 8px; margin: 16px 0 6px; }
h2 small { font-weight: normal; opacity: .85; } .chip { background: #fff; color: #1f3a5f; border-radius: 8px; padding: 0 6px; font-size: 10px; margin-right: 4px; }
.v { background: #e8eef5; border: 1px solid #c9d2dc; border-radius: 4px; padding: 0 4px; font-weight: bold; }
.card { border: 1px solid #c9d2dc; border-radius: 6px; padding: 4px 10px; margin: 6px 0; page-break-inside: avoid; } .card .n { font-weight: bold; color: #1f3a5f; }
ol { margin: 2px 0 2px 18px; padding: 0; } li { margin: 2px 0; } .dica { background: #fff4e5; border: 1px solid #ffc58b; padding: 5px 8px; border-radius: 4px; }
.abrir { margin: 4px 0; } .passo { border: 2px solid #1f3a5f; border-radius: 6px; padding: 6px 12px; margin: 8px 0; } .passo h3 { margin: 2px 0 4px; color: #1f3a5f; font-size: 13px; }'''

INICIO = '''<div class="passo"><h3>Passo 1 · Abrir o sistema</h3><ol><li>Abra no navegador (celular, iPad ou computador): <span class="v">trabalhodegest-odeprojetos.netlify.app</span></li>
<li>Vai abrir o <b>Dashboard do comitê</b>, com cartões coloridos.</li></ol></div>
<div class="passo"><h3>Passo 2 · Criar a sua conta (só na primeira vez)</h3><ol><li>No topo, toque em <span class="v">Entrar</span>.</li>
<li>Digite o <b>seu</b> e-mail e crie uma senha com pelo menos 6 caracteres.</li><li>Toque em <span class="v">Criar conta</span>.</li>
<li>Toque de novo em <span class="v">Entrar</span>, com o mesmo e-mail e senha, e toque em <span class="v">Entrar</span>.</li>
<li>Confira: no topo, onde estava "visitante (só leitura)", agora aparece o <b>seu e-mail</b>. ☐</li></ol>
<p>Cada um usa a <b>própria conta</b>: o sistema grava quem lançou cada linha, e o professor confere que pelo menos três pessoas lançaram.</p></div>
<div class="passo"><h3>Passo 3 · Ir para a tela de lançamento</h3><ol><li>No menu do topo, toque em <span class="v">Lançamentos</span>.</li>
<li>Aparece uma fileira de botões (B1, B2, B3…). Cada boletim abaixo diz em qual botão tocar.</li></ol></div>
<div class="passo"><h3>Regras de ouro</h3><ol><li><b>Uma linha por vez.</b> Preencha os campos do cartão, toque em <b>Salvar</b> e espere "Salvo em …" antes de começar a próxima.</li>
<li>Marque o ☐ de cada linha quando salvar, para não perder o lugar.</li>
<li><b>Nunca lance a mesma linha duas vezes.</b> Duplicata quebra os números de controle.</li>
<li><b>Errou?</b> Embaixo da tela tem a lista "Últimos lançamentos". Toque em <span class="v">apagar</span> na linha errada e lance de novo, certinho.</li>
<li>Campo de data: toque e escolha no calendário. Número com casas decimais: vírgula ou ponto funcionam.</li>
<li>Se o sistema mostrar um aviso perguntando "Salvar mesmo assim?", leia: se o roteiro não avisou sobre ele, cancele e confira a linha.</li></ol></div>'''

FIM = '''<div class="passo"><h3>Terminou?</h3><ol><li>Confira se todos os ☐ estão marcados.</li>
<li>Avise no grupo: "terminei os meus lançamentos".</li><li>O Diego confere tudo na página <b>Conferência</b> do sistema.</li></ol></div>'''

for nome, telas in R.PESSOAS:
    corpo = []
    total = 0
    for t in telas:
        t, linhas, comp = R.item(t)
        if t == 'quadro': corpo.append(quadro()); total += len(MOV)
        else: corpo.append(cartoes(t, linhas, comp)); total += len(linhas)
    ordem = ''
    if 'quadro' in telas:
        ordem = ('<p class="dica">⚠️ <b>Ordem obrigatória no seu lote:</b> (1) Novo item no backlog → (2) Itens da sprint → (3) Quadro da sprint. '
                 'Planejamento da sprint, Defeitos (depois do passo 1), Impedimentos e Implantações podem ser feitos a qualquer momento. Este PDF já está nessa ordem: siga de cima para baixo.</p>')
    doc = f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>Lançamentos · {nome}</title><style>{CSS}</style></head><body>
<h1>Seus lançamentos no sistema · {nome}</h1><p class="sub">G7 Plásticos Abrantes · quinzena de campo (03 a 13/11/2026) · {total} lançamentos</p>{ordem}
{INICIO}{"".join(corpo)}{FIM}</body></html>'''
    arq = os.path.join(out, f'lancamento-{nome.lower().replace("é", "e")}')
    open(arq + '.html', 'w').write(doc)
    subprocess.run(['google-chrome', '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={arq}.pdf', arq + '.html'], capture_output=True)
    os.remove(arq + '.html')
    print(nome, total, arq + '.pdf')
