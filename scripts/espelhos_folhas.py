"""Gabaritos das folhas manuscritas M1 a M8: memória de cálculo passo a passo, esboço da folha e resultado.

Uso: python scripts/gabaritos_folhas.py /tmp/m7.json docs/gabaritos
(/tmp/m7.json = fluxos dos cenários C1, C3 e C4 calculados pelo sistema, app/js/calc.js, convenções 21 a 23)
"""
import os, sys, math, json, base64, io, subprocess
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
sys.path.insert(0, os.path.dirname(__file__))
from cpm import cpm as _cpm

def cpm(ids, dur, dep):
    r, fim = _cpm(ids, dur, dep)
    return {k: {**v, 'dur': dur[k]} for k, v in r.items()}, fim

M7 = json.load(open(sys.argv[1])); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
br = lambda v, d=0: f'{v:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
pct = lambda v, d=1: br(v * 100, d) + '%'

def png(fig):
    b = io.BytesIO(); fig.savefig(b, format='png', dpi=150, bbox_inches='tight'); plt.close(fig)
    return '<img src="data:image/png;base64,' + base64.b64encode(b.getvalue()).decode() + '" style="max-width:100%">'
def tab(cab, linhas, destaque=None):
    return '<table><tr>' + ''.join(f'<th>{c}</th>' for c in cab) + '</tr>' + ''.join(
        f'<tr class="{"tot" if destaque and destaque(l) else ""}">' + ''.join(f'<td>{c}</td>' for c in l) + '</tr>' for l in linhas) + '</table>'

# ======================= M1 e M2
O = {'A32': (32, 40, 56), 'A33': (23, 28, 39), 'A34': (3, 4, 6), 'A35': (20, 25, 45), 'A38': (19, 25, 38), 'A39': (18, 22, 37), 'A40': (14, 18, 30),
     'A41': (5, 6, 9), 'A42': (12, 15, 21), 'A43': (9, 12, 17), 'A44': (4, 5, 10), 'A46': (9, 12, 22)}
DEP = [('A32', 'A33', 'II', 15), ('A32', 'A34', 'TI', 0), ('A33', 'A34', 'TI', 0), ('A33', 'A35', 'II', 10), ('A38', 'A40', 'II', 8), ('A39', 'A40', 'II', 8),
       ('A38', 'A41', 'TI', 0), ('A39', 'A41', 'TI', 0), ('A34', 'A42', 'TI', 0), ('A38', 'A42', 'TI', 0), ('A39', 'A42', 'TI', 0), ('A40', 'A43', 'TI', 0),
       ('A41', 'A43', 'TI', 0), ('A43', 'A44', 'TI', 0), ('A42', 'A46', 'TI', 0), ('A44', 'A46', 'TI', 0), ('A35', 'A46', 'TI', 0)]
TE = {k: (o + 4 * m + p) / 6 for k, (o, m, p) in O.items()}; DUR = {k: math.ceil(v - 1e-9) for k, v in TE.items()}
R1, FIM1 = cpm(list(O), DUR, DEP)
POS = {'A32': (0, 3), 'A33': (1, 3.6), 'A35': (2, 4.4), 'A34': (2, 3), 'A42': (3, 3), 'A38': (0, 1.6), 'A39': (0, 0.4), 'A40': (1, 1.6), 'A41': (1, 0.4),
       'A43': (2, 1), 'A44': (3, 1), 'A46': (4, 2.4)}

def rede(r, titulo):
    fig, ax = plt.subplots(figsize=(11, 6.2)); ax.axis('off'); W, H = 0.62, 0.62; sx, sy = 1.6, 1.25
    cen = {k: (x * sx, y * sy) for k, (x, y) in POS.items()}
    for p, s, t, l in DEP:
        (x1, y1), (x2, y2) = cen[p], cen[s]; crit = r[p]['folga'] == 0 and r[s]['folga'] == 0 and (r[s]['ES'] == (r[p]['EF'] + 1 + l if t == 'TI' else r[p]['ES'] + l))
        ax.add_patch(FancyArrowPatch((x1 + W / 2, y1), (x2 - W / 2, y2), arrowstyle='-|>', mutation_scale=10, color='#c00000' if crit else '#555', lw=2 if crit else 0.8,
                                     connectionstyle='arc3,rad=0.05'))
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.08, f'{t}{"+" + str(l) if l else ""}', fontsize=6.5, color='#1f3a5f', ha='center')
    for k, (x, y) in cen.items():
        a = r[k]; c = '#c00000' if a['folga'] == 0 else '#333'
        ax.add_patch(Rectangle((x - W / 2, y - H / 2), W, H, fill=True, fc='#fff5f5' if a['folga'] == 0 else 'white', ec=c, lw=2 if a['folga'] == 0 else 1))
        for xx in (x - W / 6, x + W / 6): ax.plot([xx, xx], [y - H / 2, y + H / 2], color=c, lw=0.5)
        ax.plot([x - W / 2, x + W / 2], [y, y], color=c, lw=0.5)
        ax.text(x, y + H / 2 + 0.05, k, ha='center', fontsize=9, weight='bold', color=c)
        for i, v in enumerate([a['ES'], a['dur'], a['EF']]): ax.text(x - W / 3 + i * W / 3, y + H / 4, str(v), ha='center', va='center', fontsize=8)
        for i, v in enumerate([a['LS'], a['folga'], a['LF']]): ax.text(x - W / 3 + i * W / 3, y - H / 4, str(v), ha='center', va='center', fontsize=8, color='#c00000' if i == 1 and v == 0 else 'black')
    ax.set_xlim(-0.6, 4 * sx + 0.6); ax.set_ylim(0, 6.2); ax.set_title(titulo, fontsize=10)
    ax.text(-0.5, 0.05, 'Caixa: em cima IC · Dur · TC; embaixo IT · Folga · TT (em dias úteis). Vermelho = caminho crítico.', fontsize=7.5)
    return png(fig)

def m1():
    linhas = [[k, *O[k], f'({O[k][0]} + 4×{O[k][1]} + {O[k][2]}) ÷ 6 = {br(TE[k], 2)}', DUR[k]] for k in O]
    ida = [[k, R1[k]['ES'], R1[k]['dur'], R1[k]['EF'], R1[k]['LS'], R1[k]['LF'], R1[k]['folga'], 'sim' if R1[k]['folga'] == 0 else ''] for k in sorted(O, key=lambda k: R1[k]['ES'])]
    return f'''<h2>Passo 1 · Duração esperada de cada atividade (convenção 1)</h2><p>Fórmula: <b>t = (O + 4M + P) ÷ 6</b>, arredondada <b>para cima</b>.</p>
{tab(['Ativ.', 'O', 'M', 'P', 'Conta', 'Duração (du)'], linhas)}
<h2>Passo 2 · Ida (início e término cedo)</h2><ul>
<li>Regra TI (término → início): início ≥ término da predecessora <b>+ 1</b> + defasagem. Regra II (início → início): início ≥ início da predecessora + defasagem. O dia útil 1 é o início da sub-rede.</li>
<li>Sem predecessora começa no du 1: A32, A38 e A39 → IC = 1. TC = IC + duração − 1 (A32: 1 + 42 − 1 = <b>42</b>).</li>
<li>A33 (II+15 de A32): IC = 1 + 15 = <b>16</b>; TC = 16 + 29 − 1 = 44. A35 (II+10 de A33): IC = 16 + 10 = 26; TC = 26 + 28 − 1 = 53.</li>
<li>A40 (II+8 de A38 e de A39): IC = 1 + 8 = 9; TC = 28. A41 (TI de A38 e A39): IC = máx(27, 24) + 1 = 28; TC = 34.</li>
<li>A34 (TI de A32 e A33): IC = máx(42, 44) + 1 = <b>45</b> → <b>quem amarra é o A33</b>, não o A32. TC = 49.</li>
<li>A42 (TI de A34, A38, A39): IC = máx(49, 27, 24) + 1 = 50; TC = 65. A43 (TI de A40 e A41): IC = máx(28, 34) + 1 = 35; TC = 47. A44: IC = 48; TC = 53.</li>
<li>A46 (TI de A42, A44, A35): IC = máx(65, 53, 53) + 1 = <b>66</b>; TC = 66 + 14 − 1 = <b>79</b> → prazo da sub-rede = <b>79 du</b>.</li></ul>
<h2>Passo 3 · Volta (término e início tarde) e folga</h2><ul>
<li>A46: TT = 79, IT = 79 − 14 + 1 = 66. Para predecessora TI: TT = IT da sucessora − 1 − defasagem; para II: IT ≤ IT da sucessora − defasagem.</li>
<li>A42 e A44 e A35: TT = 66 − 1 = 65 → A42 IT = 50; A44 IT = 60; A35 IT = 38. A43: TT = 60 − 1 = 59, IT = 47. A34: TT = 50 − 1 = 49, IT = 45.</li>
<li>A33: pela A34 (TI) TT ≤ 45 − 1 = 44; pela A35 (II+10) IT ≤ 38 − 10 = 28 → TT ≤ 28 + 29 − 1 = 56 → vale o menor: TT = 44, IT = 16.</li>
<li>A32: pela A34 TT ≤ 44; pela A33 (II+15) IT ≤ 16 − 15 = 1 → IT = 1, TT = 42. A38, A39, A40, A41 seguem do mesmo jeito (ver tabela).</li>
<li><b>Folga total = IT − IC</b>. Folga zero = crítica.</li></ul>
{tab(['Ativ.', 'IC', 'Dur', 'TC', 'IT', 'TT', 'Folga', 'Crítica'], ida, lambda l: l[7] == 'sim')}
<div class="res"><b>Resultado:</b> prazo da sub-rede = <b>79 du</b>; caminho crítico <b>A32 → A33 → A34 → A42 → A46</b>. Quase críticas: nenhuma com folga ≤ 5 du (a menor folga fora do caminho é 12 du).</div>
<h2>Esboço da folha (rede com atividade no nó)</h2>{rede(R1, 'M1 · Rede da sub-rede (atividade no nó)')}
<p class="dica">Como montar a folha (A4 deitado): à esquerda, a tabela das durações; no centro/direita, a rede desenhada com as caixas; embaixo, o resultado e a frase de interpretação. Nome e assinatura no rodapé.</p>
<h2>Interpretação (escreva na folha)</h2><p>"A sub-rede elétrica + montagem leva 79 du e é comandada pela elétrica (painéis → cabos → energização → interligação → testes a frio). Montar os equipamentos tem 12 du de folga: atrasar a montagem não atrasa os testes a frio, mas atrasar a elétrica sim."</p>'''

def m2():
    crit = ['A32', 'A33', 'A34', 'A42', 'A46']; sd = {k: (O[k][2] - O[k][0]) / 6 for k in crit}; var = sum(v * v for v in sd.values()); s = math.sqrt(var)
    z = 5 / s; P = 0.5 * (1 + math.erf(z / math.sqrt(2)))
    fig, ax = plt.subplots(figsize=(7, 3)); import numpy as np
    x = np.linspace(79 - 4 * s, 79 + 4 * s, 400); y = np.exp(-((x - 79) / s) ** 2 / 2) / (s * math.sqrt(2 * math.pi))
    ax.plot(x, y, 'k'); xx = x[x <= 84]; ax.fill_between(xx, 0, np.exp(-((xx - 79) / s) ** 2 / 2) / (s * math.sqrt(2 * math.pi)), hatch='///', facecolor='#cfe0f3', edgecolor='#1f3a5f')
    ax.axvline(79, ls='--', c='#555'); ax.axvline(84, ls='--', c='#c00000'); ax.text(79, max(y) * 1.02, 'μ = 79', ha='center'); ax.text(84, max(y) * 0.9, '84 du', color='#c00000')
    ax.text(70, max(y) * 0.35, f'P(T ≤ 84) = {pct(P)}', fontsize=10, weight='bold'); ax.set_yticks([]); ax.set_xlabel('prazo da sub-rede (du)'); ax.set_title('M2 · Prazo ~ Normal(79; 5,505)')
    return f'''<h2>Passo 1 · Desvio-padrão de cada atividade crítica</h2><p>σ = (P − O) ÷ 6 e variância = σ².</p>
{tab(['Ativ.', 'O', 'P', 'σ = (P − O) ÷ 6', 'σ²'], [[k, O[k][0], O[k][2], f'({O[k][2]} − {O[k][0]}) ÷ 6 = {br(sd[k], 3)}', br(sd[k] ** 2, 3)] for k in crit] + [['<b>Soma</b>', '', '', '', f'<b>{br(var, 3)}</b>']])}
<h2>Passo 2 · Desvio-padrão do caminho</h2><p>σ<sub>caminho</sub> = √(Σσ²) = √{br(var, 3)} = <b>{br(s, 3)} du</b>. (Soma as <b>variâncias</b>, nunca os desvios.)</p>
<h2>Passo 3 · Probabilidades</h2><ul><li>Z = (84 − 79) ÷ {br(s, 3)} = <b>{br(z, 3)}</b> → tabela normal: Φ({br(z, 2)}) ≈ <b>{pct(P)}</b> de terminar em até 84 du.</li>
<li>Exatamente no prazo calculado ou antes: Z = (79 − 79) ÷ σ = 0 → Φ(0) = <b>50%</b>.</li></ul>
<div class="res"><b>Resultado:</b> σ do caminho = {br(s, 3)} du; P(T ≤ 84 du) ≈ {pct(P)}; P(T ≤ 79 du) = 50%.</div>
<h2>Esboço (curva normal com a área hachurada)</h2>{png(fig)}
<h2>Interpretação (duas linhas, como pede o enunciado)</h2><p>"A data da rede é a média: prometê-la é ter só 50% de chance de cumprir. Para ~82% de confiança é preciso uma reserva de 5 du sobre o prazo calculado."</p>'''

# ======================= M3
E3 = [('1.1', 'Engenharia e licenças', 843912, 100, 100, 842531), ('1.2', 'Equipamentos principais', 23438568, 97.5, 93.1, 19687702), ('1.3', 'Obra civil e utilidades', 5457896, 100, 100, 6606873),
      ('1.4', 'Elétrica e automação', 2993100, 100, 58.0, 2339841), ('1.5', 'Montagem', 1726856, 0, 0, 0), ('1.6', 'Comissionamento e partida', 3253368, 0.9, 0.9, 31638),
      ('1.7', 'Pessoas e transição', 557776, 17.3, 17.3, 99634)]
AG = ('—', 'Frente ágil', 737800, 61.8, 56.7, 511078)
def m3():
    def lin(e):
        cod, n, ont, pl, av, cr = e; vp = ont * pl / 100; va = ont * av / 100
        return [cod, n, br(ont), br(vp), br(va), br(cr), br(va - vp), br(va - cr), br(va / vp, 3) if vp else '—', br(va / cr, 3) if cr else '—'], (ont, vp, va, cr)
    rows, soma = [], [0, 0, 0, 0]
    for e in E3:
        l, v = lin(e); rows.append(l); soma = [a + b for a, b in zip(soma, v)]
    ont, vp, va, cr = soma; rows.append(['', '<b>Frente preditiva</b>', br(ont), br(vp), br(va), br(cr), br(va - vp), br(va - cr), br(va / vp, 3), br(va / cr, 3)])
    la, (o2, vp2, va2, cr2) = lin(AG); rows.append(la)
    O_, VP, VA, CR = ont + o2, vp + vp2, va + va2, cr + cr2
    rows.append(['', '<b>Projeto</b>', br(O_), br(VP), br(VA), br(CR), br(VA - VP), br(VA - CR), br(VA / VP, 3), br(VA / CR, 3)])
    ENT = O_ / (VA / CR); IDPT = (O_ - VA) / (O_ - CR)
    S = {'28/02': (166.1, 127.4, 104.7), '31/03': (789.5, 466.6, 378.2), '30/04': (5176.6, 1772.2, 8475.1), '31/05': (11553.2, 7806.3, 9654.9), '30/06': (19184.3, 13856.3, 15556.7),
         '31/07': (25613.3, 21520.1, 23328.0), '31/08': (30110.1, 26861.6, 25415.1), '25/09': (32721.8, 30395.7, 30119.3)}
    fig, ax = plt.subplots(figsize=(7.5, 3.6)); k = list(S)
    for i, (n, c) in enumerate([('VP', '#2f75b5'), ('VA', '#2e7d32'), ('CR', '#c00000')]): ax.plot(k, [S[x][i] for x in k], 'o-', color=c, label=n)
    ax.set_ylabel('R$ mil (acumulado)'); ax.legend(); ax.grid(alpha=.3); ax.set_title('M3 · Curva S do projeto (duas frentes)')
    return f'''<h2>Passo 1 · Fórmulas (convenções 4 a 7)</h2><ul><li>VP = ONT × % planejado · VA = ONT × % avanço físico · CR = custo real (dado).</li>
<li>Variação de prazo VPr = VA − VP · Variação de custo VC = VA − CR · IDP = VA ÷ VP · IDC = VA ÷ CR.</li>
<li>Projeto: ENT = ONT ÷ IDC · IDPT = (ONT − VA) ÷ (ONT − CR).</li></ul>
<h2>Passo 2 · Tabela por entrega, frentes e projeto (R$)</h2>
{tab(['EAP', 'Entrega', 'ONT', 'VP', 'VA', 'CR', 'VPr', 'VC', 'IDP', 'IDC'], rows, lambda l: '<b>' in l[1])}
<p>Exemplo de conta (1.2): VP = 23.438.568 × 97,5% = {br(23438568 * .975)}; VA = 23.438.568 × 93,1% = {br(23438568 * .931)}; IDP = VA ÷ VP = {br(.931 / .975, 3)}; IDC = VA ÷ CR = {br(23438568 * .931 / 19687702, 3)}.</p>
<h2>Passo 3 · Projeto</h2><ul><li>IDC = {br(VA, 0)} ÷ {br(CR, 0)} = <b>{br(VA / CR, 3)}</b>; IDP = {br(VA, 0)} ÷ {br(VP, 0)} = <b>{br(VA / VP, 3)}</b>.</li>
<li>ENT = {br(O_)} ÷ {br(VA / CR, 3)} = <b>R$ {br(ENT)}</b>.</li><li>IDPT = ({br(O_)} − {br(VA)}) ÷ ({br(O_)} − {br(CR)}) = <b>{br(IDPT, 3)}</b>.</li></ul>
<div class="res"><b>Resultado (25/09/2026):</b> VP R$ {br(VP)} · VA R$ {br(VA)} · CR R$ {br(CR)} · IDP {br(VA / VP, 3)} · IDC {br(VA / CR, 3)} · ENT R$ {br(ENT)} · IDPT {br(IDPT, 3)}.
Confere com a curva S do dossiê (R$ mil): VP 32.721,8 · VA 30.395,7 · CR 30.119,3.</div>
<h2>Esboço (curva S em escala, R$ mil)</h2>{png(fig)}
<h2>Leitura em três linhas</h2><p>"Em 25/09 o projeto estava ligeiramente atrasado (IDP {br(VA / VP, 2)}) e ainda dentro do custo (IDC {br(VA / CR, 2)}). O atraso está na elétrica (1.4, IDP 0,58) e nos equipamentos (1.2); o estouro de custo está na obra civil (1.3, IDC 0,83). Como o IDPT ({br(IDPT, 2)}) é menor que 1, ainda havia folga de custo, que foi consumida depois pelo câmbio da injetora."</p>'''

# ======================= M4
C4 = {'A32': (42, 30, 84400), 'A33': (29, 22, 95700), 'A35': (28, 22, 42100), 'A38': (27, 21, 104400), 'A39': (24, 18, 70100), 'A40': (20, 14, 114800),
      'A42': (16, 13, 42900), 'A43': (13, 9, 36000), 'A46': (14, 12, 66700)}
def m4():
    dur = dict(DUR); passos = []; acum = 0; base = cpm(list(O), dur, DEP)[1]
    pts = [(base, 0)]
    for k in range(5):
        r, fim = cpm(list(O), dur, DEP); crit = [a for a in O if r[a]['folga'] == 0]
        melhor = None
        for a in sorted(C4, key=lambda a: C4[a][2]):
            if a not in crit or dur[a] <= C4[a][1]: continue
            d2 = dict(dur); d2[a] -= 1
            if cpm(list(O), d2, DEP)[1] < fim: melhor = a; break
        dur[melhor] -= 1; acum += C4[melhor][2]; novo = cpm(list(O), dur, DEP)[1]
        passos.append([k + 1, ' → '.join(sorted(crit, key=lambda a: r[a]['ES'])), melhor, br(C4[melhor][2]), f'{dur[melhor] + 1} → {dur[melhor]}', novo, br(acum)])
        pts.append((novo, acum))
    fig, ax = plt.subplots(figsize=(6.5, 3)); ax.plot([p[0] for p in pts], [p[1] / 1000 for p in pts], 'o-', c='#c00000', label='custo acumulado da compressão')
    ax.plot([p[0] for p in pts], [(79 - p[0]) * 50.1 for p in pts], 's--', c='#2e7d32', label='custo do atraso evitado (R$ 50,1 mil/du)')
    ax.invert_xaxis(); ax.set_xlabel('prazo da sub-rede (du)'); ax.set_ylabel('R$ mil'); ax.legend(fontsize=7); ax.grid(alpha=.3); ax.set_title('M4 · Custo acumulado × prazo')
    return f'''<h2>Regra</h2><p>Reduzir <b>um dia por vez</b>, sempre na atividade <b>crítica mais barata</b> que ainda pode ser encurtada (duração &gt; mínima) e que <b>realmente encurta a rede</b>; recalcular o caminho crítico a cada passo.</p>
<p class="dica">Pegadinha: comprimir A32 não encurta nada, porque quem amarra o A34 é o A33 (A33 termina no du 44, A32 no 42). Por isso o A32, apesar de crítico, não entra.</p>
{tab(['Opção', 'Normal', 'Mínima', 'R$/dia'], [[a, *C4[a][:2], br(C4[a][2])] for a in C4])}
<h2>Tabela de passos</h2>{tab(['Passo', 'Caminho crítico antes', 'Comprime', 'Custo do dia (R$)', 'Duração', 'Novo prazo (du)', 'Custo acumulado (R$)'], passos)}
<ul><li>Passos 1 a 3: A42 é a mais barata do caminho (R$ 42.900/dia) até chegar na mínima (16 → 13).</li>
<li>Passos 4 e 5: a próxima mais barata do caminho é A46 (R$ 66.700/dia), até 12 du. A35 (R$ 42.100) é mais barata, mas não é crítica (folga 12): comprimi-la não encurta a rede.</li>
<li>O caminho crítico não muda nos 5 passos (as outras cadeias têm folga ≥ 7 du depois da compressão).</li></ul>
<div class="res"><b>Resultado:</b> prazo 79 → <b>74 du</b>; custo total = 3 × 42.900 + 2 × 66.700 = <b>R$ {br(acum)}</b>. Custo do atraso evitado: 5 × 50.100 = R$ 250.500.</div>
<h2>Esboço (custo acumulado × prazo)</h2>{png(fig)}
<h2>Vale a pena?</h2><p>"Os 3 dias do A42 (R$ 42.900 cada) valem a pena: custam menos que o atraso (R$ 50.100/du). Os 2 dias do A46 (R$ 66.700) não: custam mais do que evitam. A compressão inteira custa R$ {br(acum)} contra R$ 250.500 de atraso evitado → só comprimir 3 dias. E atenção: hoje quem define o término do projeto é a cadeia da injetora, não a elétrica; comprimir a elétrica só ajuda se ela virar crítica."</p>'''

# ======================= M5
S13 = [('PA-139', 3, 'TRANSBORDO', '13/10', '29/10'), ('PA-140', 5, 'TRANSBORDO', '14/10', None), ('PA-187', 1, 'PLANEJAMENTO', '27/10', '29/10'), ('PA-184', 1, 'PLANEJAMENTO', '28/10', '30/10'),
       ('PA-185', 1, 'PLANEJAMENTO', '29/10', None), ('PA-186', 2, 'PLANEJAMENTO', '30/10', None), ('PA-188', 1, 'PLANEJAMENTO', '30/10', None), ('PA-141', 3, 'PLANEJAMENTO', None, None),
       ('PA-142', 5, 'PLANEJAMENTO', None, None), ('PA-143', 3, 'PLANEJAMENTO', None, None), ('PA-144', 3, 'PLANEJAMENTO', None, None), ('PA-189', 3, 'ADICIONADO_DURANTE', '20/10', '28/10'),
       ('PA-191', 2, 'ADICIONADO_DURANTE', '26/10', '30/10'), ('PA-192', 1, 'ADICIONADO_DURANTE', '26/10', None), ('PA-193', 1, 'ADICIONADO_DURANTE', '23/10', '30/10')]
DIAS = ['19/10', '20/10', '21/10', '22/10', '23/10', '26/10', '27/10', '28/10', '29/10', '30/10']
CICLO = {'PA-139': 13, 'PA-187': 3, 'PA-184': 3, 'PA-189': 7, 'PA-191': 5, 'PA-193': 6}
def m5():
    tot = sum(x[1] for x in S13); idx = {d: i for i, d in enumerate(DIAS)}
    rest = [tot - sum(x[1] for x in S13 if x[4] and idx[x[4]] <= i) for i in range(10)]; ideal = [tot * (1 - (i + 1) / 10) for i in range(10)]
    conc = [x for x in S13 if x[4]]; vel = sum(x[1] for x in conc); cm = sum(CICLO.values()) / len(CICLO); vz = len(conc) / 10
    fig, ax = plt.subplots(figsize=(7, 3.2)); ax.plot(DIAS, rest, 'o-', c='#c00000', label='real'); ax.plot(DIAS, ideal, '--', c='#555', label='ideal')
    for i, v in enumerate(rest): ax.text(i, v + 0.6, str(v), ha='center', fontsize=7)
    ax.set_ylim(0, tot + 4); ax.set_ylabel('pontos restantes'); ax.legend(); ax.grid(alpha=.3); ax.set_title('M5 · Burndown da S13')
    return f'''<h2>Passo 1 · Burndown</h2><p>Total da sprint = soma dos pontos dos 15 itens = <b>{tot} pontos</b>. Restantes no fim de cada dia útil = {tot} − pontos dos itens já concluídos. Linha ideal: de {tot} até 0 em 10 du ({br(tot / 10, 1)} por dia).</p>
{tab(['Dia', *DIAS], [['Concluídos no dia', *[' + '.join(f'{x[0]} ({x[1]})' for x in S13 if x[4] == d) or '—' for d in DIAS]], ['Restantes', *rest], ['Ideal', *[br(v, 1) for v in ideal]]])}
<h2>Passo 2 · Velocidades (convenção 8)</h2><ul><li>Velocidade da S13 = pontos concluídos = 3 + 1 + 1 + 3 + 2 + 1 = <b>{vel} pontos</b>.</li>
<li>Média das 5 últimas encerradas até 30/10 (S09 a S13, tabela 20): (5 + 13 + 25 + 16 + 11) ÷ 5 = <b>14,0 pontos/sprint</b>.</li></ul>
<h2>Passo 3 · Quantas sprints faltavam para a Release 2 em 30/10 (convenção 10)</h2><ul>
<li>Pontos restantes das releases 1 e 2 (não concluídos, prioridade ≠ WONT): R1 = 0; R2 = PA-140 5 + PA-141 3 + PA-142 5 + PA-143 3 + PA-144 3 + PA-145 3 + PA-146 2 + PA-147 8 + PA-185 1 + PA-186 2 + PA-188 1 + PA-190 2 + PA-192 1 + PA-194 1 = <b>40 pontos</b>.</li>
<li>Sprints = 40 ÷ 14,0 = 2,86 → arredonda para cima = <b>3 sprints</b> (S14, S15, S16) → Release 2 no fim da S16, <b>11/12/2026</b> (planejada para 02/10/2026).</li></ul>
<h2>Passo 4 · Fluxo (convenção 9 e Lei de Little)</h2>
{tab(['Item', 'Início', 'Conclusão', 'Tempo de ciclo (du, contando os dois extremos)'], [[k, next(x[3] for x in S13 if x[0] == k), next(x[4] for x in S13 if x[0] == k), v] for k, v in CICLO.items()])}
<ul><li>Tempo de ciclo médio = (13 + 3 + 3 + 7 + 5 + 6) ÷ 6 = <b>{br(cm, 2)} du</b> (12/10 é feriado e não conta).</li>
<li>Vazão = 6 itens concluídos ÷ 10 du = <b>{br(vz, 2)} item/du</b>.</li><li>WIP (Lei de Little) = vazão × ciclo = {br(vz, 2)} × {br(cm, 2)} = <b>{br(vz * cm, 1)} itens</b> em andamento, em média.</li></ul>
<div class="res"><b>Resultado:</b> burndown {', '.join(map(str, rest))}; velocidade S13 = {vel} pt; média = 14,0 pt; faltam 3 sprints para a R2 (11/12/2026); ciclo médio {br(cm, 2)} du; vazão {br(vz, 2)} item/du; WIP ≈ {br(vz * cm, 1)} itens.</div>
<h2>Esboço (burndown)</h2>{png(fig)}
<p class="dica">Leitura: o burndown ficou plano por 7 dias e só caiu no fim (itens grandes e muito trabalho iniciado ao mesmo tempo). Entraram 4 itens durante a sprint (7 pontos), um deles pedido direto (PA-189).</p>'''

# ======================= M6
R6 = [('R01', 'Utilidades existentes sem capacidade', 30, 283000, 12), ('R02', 'Incompatibilidade entre projetos', 37, 159000, 10), ('R04', 'Montadora alterar o desenho', 40, 850000, 20),
      ('R05', 'Interferência com a Linha de painéis', 37, 192000, 8), ('R12', 'Atraso da injetora importada', 35, 340000, 20), ('R13', 'Cabine fora do padrão de aparência', 40, 480000, 15),
      ('R14', 'Falha de comunicação CLP × supervisório', 47, 126000, 12), ('R15', 'Variação cambial', 44, 546000, 0), ('R16', 'Perda do especialista de pintura', 25, 220000, 10),
      ('R19', 'Alteração de layout após o executivo', 40, 184000, 10)]
PI = [('PI01', 'Diretor de operações', 5, 5), ('PI02', 'Gerente de produção', 4, 5), ('PI03', 'Diretor financeiro', 5, 3), ('PI04', 'Gerente de manutenção', 3, 4), ('PI05', 'Gerente de qualidade', 3, 4),
      ('PI06', 'SESMT', 4, 3), ('PI07', 'Fornecedor injetora', 3, 4), ('PI08', 'Empreiteira civil', 2, 4), ('PI09', 'Integrador de automação', 2, 4), ('PI10', 'Operadores', 1, 5),
      ('PI11', 'Sindicato', 3, 2), ('PI12', 'Órgão ambiental e Bombeiros', 5, 1), ('PI13', 'Engenharia do cliente', 5, 4), ('PI14', 'TI corporativa', 3, 3)]
ONT = 39009276
fp = lambda p: 1 if p <= 10 else 2 if p <= 30 else 3 if p <= 50 else 4 if p <= 70 else 5
fi = lambda v: (lambda f: 1 if f < .25 else 2 if f < .5 else 3 if f < 1 else 4 if f <= 2 else 5)(v / ONT * 100)
def m6():
    vme = [(r, r[2] / 100 * r[3]) for r in R6]; tot = sum(v for _, v in vme)
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.6))
    ax = axs[0]; cel = {}
    for r, _ in vme: cel.setdefault((fp(r[2]), fi(r[3])), []).append(r[0])
    for p in range(1, 6):
        for i in range(1, 6):
            s = p * i; ax.add_patch(Rectangle((i - 1, p - 1), 1, 1, fc='#f8d0d0' if s >= 12 else '#fde9c8' if s >= 6 else '#e3f1e3', ec='#777'))
            ax.text(i - 0.5, p - 0.5, '\n'.join(cel.get((p, i), [])), ha='center', va='center', fontsize=8, weight='bold')
    ax.set_xlim(0, 5); ax.set_ylim(0, 5); ax.set_xticks([.5, 1.5, 2.5, 3.5, 4.5], ['1\n<0,25%', '2\n0,25–0,5%', '3\n0,5–1%', '4\n1–2%', '5\n>2%'], fontsize=7)
    ax.set_yticks([.5, 1.5, 2.5, 3.5, 4.5], ['1 ≤10%', '2 11–30%', '3 31–50%', '4 51–70%', '5 >70%'], fontsize=7); ax.set_xlabel('impacto (% do ONT)'); ax.set_ylabel('probabilidade'); ax.set_title('Matriz probabilidade × impacto')
    ax = axs[1]; ax.axvline(3.5, c='k'); ax.axhline(3.5, c='k')
    off = {}
    for i, n, po, it in PI:
        k = (it, po); o = off.get(k, 0); off[k] = o + 1; ax.text(it + 0.03, po + 0.18 - 0.22 * o, i, fontsize=8, weight='bold')
        ax.plot(it, po, 'o', c='#1f3a5f')
    for (x, y, t) in [(5.2, 5.4, 'Gerenciar de perto'), (1.8, 5.4, 'Manter satisfeito'), (5.2, 0.6, 'Manter informado'), (1.8, 0.6, 'Monitorar')]: ax.text(x, y, t, ha='center', fontsize=8, color='#c00000')
    ax.set_xlim(0.5, 5.8); ax.set_ylim(0.3, 5.8); ax.set_xlabel('interesse'); ax.set_ylabel('poder'); ax.set_title('Matriz poder × interesse (alto = 4 ou 5)')
    q = lambda po, it: 'Gerenciar de perto' if po >= 4 and it >= 4 else 'Manter satisfeito' if po >= 4 else 'Manter informado' if it >= 4 else 'Monitorar'
    return f'''<h2>Passo 1 · Valor monetário esperado (convenção 12)</h2><p>VME = probabilidade × impacto em custo.</p>
{tab(['Id', 'Risco', 'Prob.', 'Impacto (R$)', 'VME (R$)', '% do ONT', 'Faixa P', 'Faixa I'], [[r[0], r[1], f'{r[2]}%', br(r[3]), br(v), br(r[3] / ONT * 100, 2) + '%', fp(r[2]), fi(r[3])] for r, v in vme] + [['', '<b>Total</b>', '', '', f'<b>{br(tot)}</b>', '', '', '']], lambda l: '<b>' in l[1])}
<div class="res"><b>Resultado:</b> exposição dos 10 maiores riscos = <b>R$ {br(tot)}</b> contra contingência de R$ 831.000 → <b>não cobre</b>: faltam R$ {br(tot - 831000)} ({br(tot / 831000 * 100, 0)}% da reserva).
Os maiores: R04 (desenho da montadora, R$ 340.000), R15 (câmbio, R$ 240.240) e R13 (cabine, R$ 192.000).</div>
<h2>Passo 2 · Partes interessadas (poder × interesse)</h2>{tab(['Id', 'Parte', 'Poder', 'Interesse', 'Quadrante / estratégia'], [[a, b, c, d, q(c, d)] for a, b, c, d in PI])}
<ul><li><b>Gerenciar de perto</b> (PI01, PI02, PI13): reuniões frequentes, decisões juntas. PI13 (montadora) é crítica: pede mudanças direto ao time ágil.</li>
<li><b>Manter satisfeito</b> (PI03, PI06, PI12): relatórios de custo, segurança e licenças nos marcos, sem excesso de detalhe.</li>
<li><b>Manter informado</b> (PI04, PI05, PI07, PI08, PI09, PI10): comunicação regular, treinamento e participação nos testes.</li><li><b>Monitorar</b> (PI11, PI14): acompanhar sem esforço grande.</li></ul>
<h2>Esboço (as duas matrizes na mesma folha)</h2>{png(fig)}
<p class="dica">Observação para a arguição: R15 já se materializou (câmbio, R$ 812 mil) e consumiu a contingência inteira; por isso a reserva hoje tem saldo negativo no sistema.</p>'''

# ======================= M7
def m7():
    linhas = []
    for c, nome in [('C1', 'Seguir como está'), ('C3', 'Cortar escopo'), ('C4', 'Ampliar o escopo')]:
        r = M7[c]; a = r['anos']
        cab = f'<h3>{c} · {nome} — término {"/".join(reversed(r["termino"].split("-")))}, {r["du"]} du além do contrato, atraso = {br(r["meses"], 2)} mês</h3>'
        t = tab(['Ano', 'Benefício', 'Custo operac.', 'Investimento', 'Fluxo líquido', 'Fator 1,14^ano', 'Valor presente', 'Acumulado'],
                [[x['ano'], br(x['ben']), br(x['op']), br(x['inv']), br(x['fluxo']), br(1.14 ** x['ano'], 4), br(x['fluxo'] / 1.14 ** x['ano']), br(x['acumulado'])] for x in a])
        a1 = a[1]
        linhas.append(cab + f'''<ul><li>Ano 0 = 43.007.000 + (ENT − ONT) = 43.007.000 + ({br(r["ent"])} − 39.009.276) = <b>{br(a[0]["inv"])}</b>.</li>
<li>Benefício × (1 {"+" if r["varBen"] >= 0 else "−"} {br(abs(r["varBen"]), 1)}%) e custo operacional {"+" if r["varOp"] >= 0 else "−"} R$ {br(abs(r["varOp"]))}/ano (tabela 43).</li>
<li>Atraso: meses = dias corridos entre 27/04/2027 e o término ÷ 30,4 = {br(r["meses"], 4)}; perda no ano 1 = fluxo do ano 1 × meses ÷ 12 = {br(a1["perdaAtraso"])}.</li></ul>{t}
<p><b>VPL</b> = Σ valor presente = <b>R$ {br(r["vpl"])}</b> · <b>Payback</b> = {int(r["payback"])} + |acumulado do ano {int(r["payback"])}| ÷ fluxo do ano {int(r["payback"]) + 1} = <b>{br(r["payback"], 2)} anos</b> ·
custo do atraso = {r["du"]} × 50.100 = R$ {br(r["custoAtraso"])} · <b>Resultado = VPL − atraso = R$ {br(r["resultado"])}</b></p>''')
    fig, ax = plt.subplots(figsize=(7.5, 3.4))
    for c, cor in [('C1', '#2f75b5'), ('C3', '#c00000'), ('C4', '#2e7d32')]: ax.plot([x['ano'] for x in M7[c]['anos']], [x['acumulado'] / 1e6 for x in M7[c]['anos']], 'o-', c=cor, label=c)
    ax.axhline(0, c='k', lw=.8); ax.set_xlabel('ano'); ax.set_ylabel('acumulado (R$ mi)'); ax.legend(); ax.grid(alpha=.3); ax.set_title('M7 · Fluxo de caixa acumulado')
    res = tab(['Cenário', 'Término', 'ENT', 'VPL', 'Payback', 'Custo do atraso', 'Resultado'], [[c, '/'.join(reversed(M7[c]['termino'].split('-'))), br(M7[c]['ent']), br(M7[c]['vpl']), br(M7[c]['payback'], 2), br(M7[c]['custoAtraso']), br(M7[c]['resultado'])] for c in ['C1', 'C3', 'C4']])
    return f'''<h2>Regras (convenções 16 e 23)</h2><ul><li>Fluxo do ano = benefício − custo operacional − investimento. VPL a 14% a.a.: VP do ano t = fluxo ÷ 1,14<sup>t</sup>.</li>
<li>O cenário muda: o ano 0 (soma ENT − ONT), o benefício (%), o custo operacional (R$/ano) e o ano 1 (perde a fração dos meses de atraso).</li>
<li>Payback simples com interpolação dentro do ano. Resultado = VPL − custo do atraso (R$ 50.100 por du além de 07/05/2027).</li></ul>
{''.join(linhas)}<div class="res"><b>Resumo:</b>{res}</div>
<h2>Esboço (fluxo acumulado dos três cenários)</h2>{png(fig)}
<p>Leitura: "O C4 tem o maior VPL (o benefício sobe 4%), mas o atraso de 32 du custa R$ 1,6 mi e derruba o resultado. O C3 corta custo, mas perde benefício e tem o pior resultado. Entre os três, seguir como está (C1) é o melhor; no simulador, o C6 supera o C1."</p>'''

# ======================= M8
def m8():
    P = [('P09 Caio', 'CLT', 9000, 72, 1650, 62.5, 0), ('P15 Fábio', 'PJ', 20830, 0, 0, 116.0, 0), ('P01 Leandro', 'CLT', 13500, 72, 1650, 152.0, 0)]
    a = [[n, v, f'{br(r)} × (1 + {e}%) + {br(b)} = <b>{br(r * (1 + e / 100) + b, 2)}</b>', f'{br(r * (1 + e / 100) + b, 2)} ÷ 168 = {br((r * (1 + e / 100) + b) / 168, 2)} → <b>{round((r * (1 + e / 100) + b) / 168)}</b>',
          f'{br(hn, 1)} × {round((r * (1 + e / 100) + b) / 168)} = <b>{br(hn * round((r * (1 + e / 100) + b) / 168), 2)}</b>'] for n, v, r, e, b, hn, he in P]
    H9 = {'02/26': (0, 0), '03/26': (0, 0), '04/26': (7, 0), '05/26': (48, 43), '06/26': (45, 52), '07/26': (3, 48), '08/26': (67, 48), '09/26': (46, 50), '10/26': (0, 62)}
    H15 = {'05/26': (160, 160), '06/26': (160, 176), '07/26': (176, 160), '08/26': (168, 215), '09/26': (168, 66), '10/26': (168, 116)}
    def hist(H, t):
        fig, ax = plt.subplots(figsize=(6, 2.6)); import numpy as np; k = list(H); x = np.arange(len(k))
        ax.bar(x - .2, [H[m][0] for m in k], .4, label='planejadas', color='#9db7d3'); ax.bar(x + .2, [H[m][1] for m in k], .4, label='apontadas', color='#1f3a5f')
        for i, m in enumerate(k):
            p, r = H[m]
            if (p and abs(r - p) / p > .2) or (not p and r): ax.text(i, max(p, r) + 4, '⚠', ha='center', color='#c00000', fontsize=11)
        ax.set_xticks(x, k); ax.legend(fontsize=7); ax.set_title(t); ax.set_ylabel('h'); return png(fig)
    dv = lambda H: [[m, p, r, r - p, (pct((r - p) / p, 0) if p else ('sem plano' if r else '—')), '⚠' if (p and abs(r - p) / p > .2) or (not p and r) else ''] for m, (p, r) in H.items()]
    A = [('A33', 'm', 11401.0, 7879.0, 1680, 6.180, 8, 6.3, 6.2), ('A39', 't', 82.0, 72.0, 1310, 0.043, 10, 9.5, 9.7)]
    c = []
    for i, u, q, ex, hh, pp, eq, e3, em in A:
        pr = ex / hh; ip = pr / pp; ie = em / eq; rest = q - ex; d = rest / (pr * e3 * 8)
        c.append([i, f'{br(ex, 0)} ÷ {br(hh)} = <b>{br(pr, 3)}</b> {u}/Hh', f'{br(pr, 3)} ÷ {br(pp, 3)} = <b>{br(ip, 3)}</b>', f'{br(em, 1)} ÷ {eq} = <b>{br(ie, 3)}</b>',
                  f'{br(rest, 0)} ÷ ({br(pr, 3)} × {br(e3, 1)} × 8) = {br(d, 2)} → <b>{math.ceil(d - 1e-9)} du</b>'])
    return f'''<h2>(a) Custo de pessoal (convenção 17)</h2><p>Custo mensal = remuneração × (1 + encargos) + benefícios; custo/hora = mensal ÷ 168 h, arredondado; outubro = horas × custo/hora (hora extra × 1,5; aqui não houve).</p>
{tab(['Pessoa', 'Vínculo', 'Custo mensal (R$)', 'Custo/hora (R$) → confere com a tab. 04', 'Custo em out/26 (R$)'], a)}
<h2>(b) Histograma planejado × apontado (desvio &gt; 20% marcado)</h2>{tab(['P09 mês', 'Planejado', 'Apontado', 'Desvio (h)', 'Desvio (%)', ''], dv(H9))}{hist(H9, 'P09 Caio · horas por mês')}
{tab(['P15 mês', 'Planejado', 'Apontado', 'Desvio (h)', 'Desvio (%)', ''], dv(H15))}{hist(H15, 'P15 Fábio · horas por mês')}
<p>P09: desvios &gt; 20% em 04/26, 07/26, 08/26 e 10/26 (trabalhou sem horas planejadas em julho e outubro: a elétrica atrasou e invadiu meses sem plano). P15: 08/26 (+28%), 09/26 (−61%) e 10/26 (−31%).</p>
<h2>(c) Produtividade (convenção 20)</h2>{tab(['Ativ.', 'Produtividade real', 'Índice de produtividade', 'Índice de efetivo', 'Duração restante'], c)}
<div class="res"><b>Resultado:</b> custos/hora 102, 124 e 148 (conferem com a tabela 04). A33: índice de produtividade 0,759 e de efetivo 0,775 → <b>falta gente e falta produtividade</b> (as duas causas, ~24% abaixo do plano cada), restam 15 du.
A39: produtividade 28% acima do plano e efetivo 97% → <b>não há problema</b>, restam 3 du.</div>'''

# ======================= montar ESPELHOS (folha A4 quadriculada, como deve ficar à mão)
CSS = '''@page { size: A4; margin: 0; } body { margin: 0; font-family: "DejaVu Sans", Arial, sans-serif; color: #1a2b6d; }
.pg { width: 210mm; min-height: 297mm; box-sizing: border-box; padding: 9mm 10mm; font-size: 9.3px; line-height: 1.42;
 background-image: linear-gradient(#c9dcef 1px, transparent 1px), linear-gradient(90deg, #c9dcef 1px, transparent 1px); background-size: 5mm 5mm; }
.cab { display: flex; justify-content: space-between; border-bottom: 1.5px solid #1a2b6d; padding-bottom: 3px; margin-bottom: 5px; }
h1 { font-size: 14px; margin: 0; } h2 { font-size: 11px; margin: 9px 0 3px; text-decoration: underline; color: #1a2b6d; background: none; padding: 0; }
h3 { font-size: 10px; margin: 7px 0 2px; color: #1a2b6d; } table { border-collapse: collapse; width: 100%; margin: 3px 0 5px; background: rgba(255,255,255,.4); }
th, td { border: 1px solid #1a2b6d; padding: 1px 3px; text-align: center; vertical-align: top; font-size: 8.3px; } tr.tot td { font-weight: bold; }
.res { border: 1.5px solid #1a2b6d; padding: 5px 7px; margin: 6px 0; background: rgba(255,255,255,.4); } .dica { border: 1px dashed #1a2b6d; padding: 4px 7px; }
ul { margin: 2px 0 4px 16px; padding: 0; } li { margin: 2px 0; } p { margin: 3px 0; } img { display: block; margin: 4px auto; max-width: 92% !important; }
.ass { margin-top: 14px; display: flex; gap: 30px; } .ass div { flex: 1; border-top: 1px solid #1a2b6d; padding-top: 2px; text-align: center; font-size: 8.5px; }
.aviso { display: none; }'''
NOME = {'Caique': ('Caique Mattos', '220115794'), 'José': ('João José Sousa', '222118958'), 'Marjorie': ('Marjorie Santos', '224215260'),
        'Guilherme': ('Guilherme Rosa', '222115955'), 'Arley': ('Arley Piana', '222118949'), 'Diego': ('Diego de Souza', '222215124')}
FOLHAS = [('M1', 'Rede e caminho crítico', 'Caique', m1), ('M2', 'Incerteza do prazo', 'Caique', m2), ('M3', 'Valor agregado em 25/09/2026', 'José', m3),
          ('M4', 'Compressão do cronograma', 'Marjorie', m4), ('M5', 'Sprint S13 e fluxo', 'Guilherme', m5), ('M6', 'Riscos e partes interessadas', 'Marjorie', m6),
          ('M8', 'Pessoas e produtividade', 'Arley', m8)]
for cod, tit, quem, f in FOLHAS:
    n, mat = NOME[quem]
    html = f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>{cod} espelho</title><style>{CSS}</style></head><body><div class="pg">
<div class="cab"><div><h1>Folha {cod} · {tit}</h1>ENGN62 · G7 Plásticos Abrantes · data de status 13/11/2026</div><div style="text-align:right">{n} · mat. {mat}</div></div>
{f()}<div class="ass"><div>{n} · assinatura</div><div>Data: 24/11/2026</div></div></div></body></html>'''
    arq = os.path.join(OUT, f'{cod}-espelho-da-folha')
    open(arq + '.html', 'w').write(html)
    subprocess.run(['google-chrome', '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={arq}.pdf', arq + '.html'], capture_output=True)
    os.remove(arq + '.html'); print(cod, arq + '.pdf')
