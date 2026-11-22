"""Gera o roteiro de lançamento dos boletins (HTML pronto para virar PDF), por integrante.

Uso: python scripts/roteiro_lancamento.py docs/roteiro-lancamento.html
Os dados vêm de testes/boletins_dados.py, os mesmos que o teste automático lança e confere.
"""
import os, re, sys, html
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'testes'))
from boletins_dados import B, MOV

telas_js = open(os.path.join(os.path.dirname(__file__), '..', 'app', 'js', 'telas.js')).read()
BLOCOS = dict(re.findall(r"^  (\w+): \{ bol: '[^']+',(.*?)(?=^  \w+: \{ bol:|^\};)", telas_js, re.M | re.S))
ROTT = {k: dict(re.findall(r"\['(\w+)', '([^']+)', '(?:data|int|num|txt|sel)'", v)) for k, v in BLOCOS.items()}
TIT = dict(re.findall(r"^  (\w+): \{ bol: '(?:B\d+)', titulo: '([^']+)'", telas_js, re.M))
BOL = dict(re.findall(r"^  (\w+): \{ bol: '(B\d+)'", telas_js, re.M))
SN = {'situacao': {'EM_ANDAMENTO': 'Em andamento', 'CONCLUIDA': 'Concluída'}, 'falhou': {'0': 'não', '1': 'sim'}, 'patrocinador_presente': {'0': 'não', '1': 'sim'}, 'ata_publicada': {'0': 'não', '1': 'sim'}}

def fmt(c, v):
    if c in SN: return SN[c][v]
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', v): return '/'.join(reversed(v.split('-')))
    return v.replace('.', ',') if re.fullmatch(r'-?\d+\.\d+', v) else v

PESSOAS = [
    ('Caique', ['avanco']),
    ('José', ['horas', 'custos', 'medicoes']),
    ('Marjorie', ['inspecoes', 'mudancas']),
    ('Guilherme', ['sprint', 'backlog', 'itemSprint', 'defeitos', 'quadro', 'impedimentos', 'implantacoes']),
    ('Arley', ['reunioes', 'engajamento', 'pulso', 'okr', 'producao', 'funil']),
]

def tabela(tela):
    ROT = ROTT[tela]
    linhas = B[tela]; cols = []
    for l in linhas:
        for c in l:
            if c not in cols: cols.append(c)
    th = ''.join(f'<th>{html.escape(ROT.get(c, c))}</th>' for c in cols)
    tr = ''.join('<tr><td class="n">' + str(i + 1) + '</td>' + ''.join(f'<td>{html.escape(fmt(c, l[c])) if c in l else "<i>vazio</i>"}</td>' for c in cols) + '</tr>' for i, l in enumerate(linhas))
    return f'<table><tr><th>#</th>{th}</tr>{tr}</table>'

def quadro():
    tr = ''.join(f'<tr><td class="n">{i + 1}</td><td>{fmt("d", d)}</td><td>{it}</td><td><b>{para.replace("_", " ")}</b></td><td>{q}</td><td>{"" if r is None else ("sim" if r == "1" else "não")}</td></tr>'
                 for i, (d, it, para, q, r) in enumerate(MOV))
    return ('<p class="dica">Antes de cada movimento, ajuste no topo da tela: <b>Data do movimento</b>, <b>Quem moveu</b> e, só quando for para EM REVISAO, <b>Revisão por par</b>. '
            'Depois, no cartão do item, escolha a nova coluna na listinha. Faça <b>exatamente nesta ordem</b>: um item passa por várias colunas.</p>'
            f'<table><tr><th>#</th><th>Data</th><th>Item</th><th>Mover para</th><th>Quem moveu</th><th>Revisão por par</th></tr>{tr}</table>')

AVISO = {
    'medicoes': 'MED-CT11-06 já existe: preencha só o código e os campos do pagamento. As duas do CT10 são novas: preencha tudo.',
    'backlog': 'Faça esta tela ANTES de "Itens da sprint": o PA-195 precisa existir para entrar na S14. O sistema vai avisar que PEDIDO_DIRETO é escopo sem controle de mudança: confirme (é o que aconteceu).',
    'mudancas': 'SM-013 já existe (estava EM ANÁLISE): use o mesmo código e o sistema atualiza a decisão.',
    'okr': 'Cada KR tem duas medições no boletim: a 1ª vai com data 31/10/2026 e a 2ª com 13/11/2026 (premissa do grupo).',
    'impedimentos': 'IP-008 e IP-009 continuam abertos: deixe Fechamento e Dias úteis vazios.',
    'horas': 'Item: código da atividade (A12), da sprint (S14) ou GESTAO. Horas extras = 0 em todas.',
}

def main():
    partes = []
    for nome, telas in PESSOAS:
        blocos = []
        for t in telas:
            if t == 'quadro':
                blocos.append(f'<h3><span class="chip">B6</span> Quadro da sprint (mover cartões) · {len(MOV)} movimentos</h3>{quadro()}')
                continue
            aviso = f'<p class="dica">{AVISO[t]}</p>' if t in AVISO else ''
            blocos.append(f'<h3><span class="chip">{BOL[t]}</span> {html.escape(TIT[t])} · {len(B[t])} linha(s)</h3>{aviso}{tabela(t)}')
        partes.append(f'<section><h2>{nome}</h2>{"".join(blocos)}</section>')

    doc = f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>Roteiro de lançamento dos boletins · G7</title><style>
    @page {{ size: A4 landscape; margin: 10mm; }}
    body {{ font-family: "DejaVu Sans", Arial, sans-serif; font-size: 10.5px; color: #1d2733; }}
    h1 {{ font-size: 18px; margin: 0 0 4px; color: #1f3a5f; }} h2 {{ font-size: 16px; color: #fff; background: #1f3a5f; padding: 5px 8px; margin: 0 0 6px; }}
    h3 {{ font-size: 12px; color: #1f3a5f; margin: 10px 0 4px; }} section {{ page-break-before: always; }}
    table {{ border-collapse: collapse; width: 100%; margin-bottom: 4px; }} th {{ background: #e8eef5; }} th, td {{ border: 1px solid #c9d2dc; padding: 3px 4px; text-align: left; vertical-align: top; }}
    td.n {{ color: #6b7785; width: 18px; }} .chip {{ background: #1f3a5f; color: #fff; border-radius: 8px; padding: 0 6px; font-size: 10px; }}
    .dica {{ background: #fff4e5; border: 1px solid #ffc58b; padding: 4px 6px; margin: 3px 0; }} ol {{ margin: 4px 0 0 16px; padding: 0; }} li {{ margin: 3px 0; }}
    .caixa {{ border: 1px solid #c9d2dc; border-radius: 6px; padding: 6px 10px; margin-top: 6px; }}
    </style></head><body>
    <h1>Roteiro de lançamento dos boletins · G7 Plásticos Abrantes</h1>
    <p>Sistema: <b>https://trabalhodegest-odeprojetos.netlify.app</b> → menu <b>Lançamentos</b>. Data de status: 13/11/2026.</p>
    <div class="caixa"><b>Antes de começar (cada um, uma vez):</b><ol>
    <li>Abra o sistema, toque em <b>Entrar</b> → digite o <b>seu</b> e-mail e uma senha (mínimo 6 caracteres) → <b>Criar conta</b>. Depois <b>Entrar</b>. No topo deve aparecer o seu e-mail.</li>
    <li>Em <b>Lançamentos</b>, toque na aba da tela (os botões com B1, B2…). Preencha <b>uma linha da tabela por vez</b> e toque em <b>Salvar</b>. Espere a mensagem "Salvo em…" antes da próxima.</li>
    <li>Campos marcados como <i>vazio</i>: deixe em branco ou escolha "— vazio —". Datas no formato do iPad/celular; números com vírgula ou ponto.</li>
    <li><b>Errou?</b> Na lista "Últimos lançamentos" embaixo da tela, toque em <b>apagar</b> na linha errada e lance de novo. <b>Nunca lance a mesma linha duas vezes</b>: duplicata quebra os números de controle.</li>
    <li>Ordem entre pessoas: o <b>Guilherme</b> faz "Novo item no backlog" antes de "Itens da sprint" e do quadro. As outras telas podem ser feitas em qualquer ordem, ao mesmo tempo.</li>
    <li>No fim, o <b>Diego</b> abre <b>Conferência</b>: as 13 linhas da coluna "até 13/11" devem ficar com ✔ confere.</li></ol></div>
    {"".join(partes)}
    </body></html>'''
    open(sys.argv[1], 'w').write(doc)
    print('ok', sys.argv[1])

if __name__ == '__main__':
    main()
