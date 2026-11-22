"""Teste de ponta a ponta: lança os boletins B1 a B10 do dossiê PELAS TELAS do sistema (navegador real)
e confere os números de controle de 13/11/2026 na página de Conferência.

Uso: python testes/teste_boletins.py   (com o servidor de teste rodando: python testes/servidor.py app testes/mock)
Serve também de roteiro: mostra, tela por tela, o que digitar de cada boletim.
"""
from playwright.sync_api import sync_playwright

from boletins_dados import URL, B, MOV

erros = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 1000})
    pg.on('pageerror', lambda e: erros.append('PAGEERROR ' + str(e)))
    pg.on('dialog', lambda d: d.accept())
    pg.goto(URL + '/#/lancamentos'); pg.wait_for_selector('.abas button', timeout=30000)
    ordem = ['avanco', 'horas', 'custos', 'medicoes', 'inspecoes', 'sprint', 'backlog', 'itemSprint', 'defeitos', 'impedimentos', 'implantacoes', 'mudancas',
             'reunioes', 'engajamento', 'pulso', 'okr', 'producao', 'funil']
    for tela in ordem:
        for linha in B[tela]:
            pg.click(f'button[data-t="{tela}"]'); f = pg.locator(f'#tela form.lanc[data-tela="{tela}"]'); f.wait_for(timeout=15000)
            for campo, valor in linha.items():
                el = f.locator(f'[name="{campo}"]')
                if el.evaluate('e => e.tagName') == 'SELECT': el.select_option(valor)
                else: el.fill(valor)
            n0 = pg.locator('#recentes tr').count()
            f.locator('button:has-text("Salvar")').click()
            pg.wait_for_function('() => document.querySelector("#toast").style.display==="block"', timeout=30000)
            txt = pg.locator('#toast').inner_text(); pg.evaluate('document.querySelector("#toast").style.display="none"')
            if not txt.startswith('Salvo'): erros.append(f'{tela}: {txt} {linha}')
        print('ok', tela, len(B[tela]))
    # B6 · quadro
    pg.click('button[data-t="quadro"]'); pg.wait_for_selector('#colunas .cartaoItem', timeout=15000)
    pg.select_option('#spQ', 'S14'); pg.wait_for_timeout(500)
    for data, item, para, quem, rev in MOV:
        pg.fill('#movForm input[name=data]', data); pg.select_option('#movForm select[name=pessoa]', quem)
        if rev is not None: pg.select_option('#movForm select[name=rev]', rev)
        pg.locator(f'.cartaoItem[data-i="{item}"] select.para').select_option(para)
        pg.wait_for_function(f'() => document.querySelector(".cartaoItem[data-i=\\"{item}\\"]") && document.querySelector(".cartaoItem[data-i=\\"{item}\\"]").closest(".coluna").querySelector("h4").textContent === "{para.replace("_", " ")}"', timeout=15000)
    print('ok quadro', len(MOV))
    pg.goto(URL + '/#/conferencia'); pg.wait_for_selector('table', timeout=30000); pg.wait_for_timeout(1500)
    for tr in pg.locator('.cartao').first.locator('tbody tr').all(): print(' | '.join(tr.locator('td').all_inner_texts()))
    print(pg.locator('.cartao').nth(1).inner_text())
    pg.goto(URL + '/#/dashboard'); pg.wait_for_selector('.kpi', timeout=30000); pg.wait_for_timeout(1000)
    print(' || '.join(t.replace('\n', ' ') for t in pg.locator('.kpi').all_inner_texts()))
    pg.screenshot(path='/tmp/dash13.png', full_page=True)
    b.close()
print('ERROS:', erros)
