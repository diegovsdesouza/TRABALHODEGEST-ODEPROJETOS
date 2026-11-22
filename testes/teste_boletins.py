"""Teste de ponta a ponta: lança os boletins B1 a B10 do dossiê PELAS TELAS do sistema (navegador real)
e confere os números de controle de 13/11/2026 na página de Conferência.

Uso: python testes/teste_boletins.py   (com o servidor de teste rodando: python testes/servidor.py app testes/mock)
Serve também de roteiro: mostra, tela por tela, o que digitar de cada boletim.
"""
from playwright.sync_api import sync_playwright

URL = 'http://127.0.0.1:8765'
B = {
 'avanco': [dict(semana_fim='2026-11-06', id_atividade='A12', avanco_acumulado_pct='50', situacao='EM_ANDAMENTO', data_inicio_real='2026-10-20'),
            dict(semana_fim='2026-11-06', id_atividade='A33', avanco_acumulado_pct='80', situacao='EM_ANDAMENTO', data_inicio_real='2026-09-14'),
            dict(semana_fim='2026-11-06', id_atividade='A35', avanco_acumulado_pct='95', situacao='EM_ANDAMENTO', data_inicio_real='2026-09-29'),
            dict(semana_fim='2026-11-06', id_atividade='A39', avanco_acumulado_pct='90', situacao='EM_ANDAMENTO', data_inicio_real='2026-10-07'),
            dict(semana_fim='2026-11-13', id_atividade='A12', avanco_acumulado_pct='70', situacao='EM_ANDAMENTO', data_inicio_real='2026-10-20'),
            dict(semana_fim='2026-11-13', id_atividade='A33', avanco_acumulado_pct='90', situacao='EM_ANDAMENTO', data_inicio_real='2026-09-14'),
            dict(semana_fim='2026-11-13', id_atividade='A35', avanco_acumulado_pct='100', situacao='CONCLUIDA', data_inicio_real='2026-09-29', data_termino_real='2026-11-09'),
            dict(semana_fim='2026-11-13', id_atividade='A39', avanco_acumulado_pct='100', situacao='CONCLUIDA', data_inicio_real='2026-10-07', data_termino_real='2026-11-10')],
 'horas': [dict(semana_inicio=s, id_pessoa=p, tipo_item=t, id_item=i, horas_normais=h, horas_extras='0') for s, rows in [
     ('2026-11-02', [('P01', 'GESTAO', 'GESTAO', '32'), ('P02', 'GESTAO', 'GESTAO', '32'), ('P03', 'GESTAO', 'GESTAO', '32'), ('P06', 'ATIVIDADE', 'A12', '10.5'),
                     ('P08', 'ATIVIDADE', 'A39', '16'), ('P09', 'ATIVIDADE', 'A33', '13'), ('P10', 'ATIVIDADE', 'A35', '14.5'), ('P13', 'SPRINT', 'S14', '32'),
                     ('P14', 'SPRINT', 'S14', '32'), ('P15', 'SPRINT', 'S14', '32'), ('P16', 'SPRINT', 'S14', '32'), ('P17', 'SPRINT', 'S14', '16')]),
     ('2026-11-09', [('P01', 'GESTAO', 'GESTAO', '40'), ('P02', 'GESTAO', 'GESTAO', '40'), ('P03', 'GESTAO', 'GESTAO', '40'), ('P06', 'ATIVIDADE', 'A12', '13.5'),
                     ('P08', 'ATIVIDADE', 'A39', '8'), ('P09', 'ATIVIDADE', 'A33', '16.5'), ('P10', 'ATIVIDADE', 'A35', '3.5'), ('P13', 'SPRINT', 'S14', '40'),
                     ('P14', 'SPRINT', 'S14', '40'), ('P15', 'SPRINT', 'S14', '40'), ('P16', 'SPRINT', 'S14', '40'), ('P17', 'SPRINT', 'S14', '20')])] for p, t, i, h in rows],
 'custos': [dict(data='2026-11-05', frente='GESTAO', categoria_custo='INDIRETO', documento='NF-GES-2611-45', descricao='Escritório do projeto, veículos e comunicação', valor_rs='36054.15'),
            dict(data='2026-11-09', frente='PREDITIVA', categoria_custo='SERVICO_CONTRATADO', id_atividade='A35', id_contrato='CT10', id_fornecedor='F10', documento='MED-CT10-03', descricao='Medição de 11/2026 — Instalar a instrumentação e a rede industrial', valor_rs='47401.51'),
            dict(data='2026-11-09', frente='PREDITIVA', categoria_custo='MATERIAL', id_atividade='A35', id_contrato='CT10', id_fornecedor='F10', documento='MED-CT10-06', descricao='Medição de 11/2026 — Instalar a instrumentação e a rede industrial', valor_rs='37739.31'),
            dict(data='2026-11-11', frente='PREDITIVA', categoria_custo='SERVICO_CONTRATADO', id_atividade='A39', id_contrato='CT11', id_fornecedor='F11', documento='MED-CT11-06', descricao='Medição final e aceite — Montar: Cabine de pintura robotizada', valor_rs='151320.00'),
            dict(data='2026-11-11', frente='AGIL', categoria_custo='LICENCAS_E_NUVEM', documento='NF-NUV-2611', descricao='Licenças de software industrial e servidor', valor_rs='17171.31'),
            dict(data='2026-11-12', frente='GESTAO', categoria_custo='INDIRETO', documento='NF-GES-2611-30', descricao='Seguros, taxas e auditorias', valor_rs='25035.01')],
 'medicoes': [dict(id_medicao='MED-CT10-03', id_contrato='CT10', id_atividade='A35', descricao_marco='Medição de 11/2026 — Instalar a instrumentação e a rede industrial', data_prevista='2026-11-09', valor_previsto_rs='46767.86', data_real='2026-11-09', valor_pago_rs='47401.51', aceite='APROVADO', nao_conformidades='0'),
              dict(id_medicao='MED-CT10-06', id_contrato='CT10', id_atividade='A35', descricao_marco='Medição de 11/2026 — Instalar a instrumentação e a rede industrial', data_prevista='2026-11-09', valor_previsto_rs='36375.00', data_real='2026-11-09', valor_pago_rs='37739.31', aceite='APROVADO', nao_conformidades='0'),
              dict(id_medicao='MED-CT11-06', data_real='2026-11-11', valor_pago_rs='151320.00', aceite='APROVADO', nao_conformidades='0')],
 'inspecoes': [dict(data='2026-11-04', id_atividade='A12', tipo_inspecao='LISTA_DE_VERIFICACAO', itens_verificados='57', itens_nao_conformes='2', resultado='APROVADO', id_fornecedor='F06', horas_retrabalho='14.0', custo_retrabalho_rs='1948.01'),
               dict(data='2026-11-04', id_atividade='A33', tipo_inspecao='LISTA_DE_VERIFICACAO', itens_verificados='60', itens_nao_conformes='4', resultado='APROVADO_COM_RESSALVA', id_fornecedor='F09', horas_retrabalho='24.8', custo_retrabalho_rs='3607.98'),
               dict(data='2026-11-05', id_atividade='A35', tipo_inspecao='LISTA_DE_VERIFICACAO', itens_verificados='26', itens_nao_conformes='1', resultado='APROVADO', id_fornecedor='F10', horas_retrabalho='6.4', custo_retrabalho_rs='804.60'),
               dict(data='2026-11-06', id_atividade='A39', tipo_inspecao='LISTA_DE_VERIFICACAO', itens_verificados='53', itens_nao_conformes='0', resultado='APROVADO', id_fornecedor='F11', horas_retrabalho='0', custo_retrabalho_rs='0')],
 'sprint': [dict(id_sprint='S14', pessoas_dia_disponiveis='18', horas_extras_autorizadas='NAO', meta_da_sprint='Avançar o épico Receitas, setup e ordens de produção')],
 'backlog': [dict(id_item='PA-195', data_criacao='2026-11-04', tipo_item='HISTORIA', id_epico='EP01', titulo='Gerar um relatório extra para a reunião de produção', pontos='2', prioridade_moscow='SHOULD', id_release='R2', origem='PEDIDO_DIRETO', id_solicitante='PI13'),
             dict(id_item='PA-196', data_criacao='2026-11-05', tipo_item='BUG', id_epico='EP03', titulo='Corrigir a falha em: Configurar o monitoramento e os registros: Rastreabilidade de lotes e qualidade', pontos='2', prioridade_moscow='MUST', id_release='R2', origem='DEFEITO')],
 'itemSprint': [dict(id_sprint='S14', id_item=i, origem_na_sprint=o) for i, o in [('PA-140', 'TRANSBORDO'), ('PA-185', 'TRANSBORDO'), ('PA-186', 'TRANSBORDO'), ('PA-188', 'TRANSBORDO'),
     ('PA-192', 'TRANSBORDO'), ('PA-194', 'PLANEJAMENTO'), ('PA-190', 'PLANEJAMENTO'), ('PA-141', 'PLANEJAMENTO'), ('PA-142', 'PLANEJAMENTO'), ('PA-143', 'PLANEJAMENTO'),
     ('PA-144', 'PLANEJAMENTO'), ('PA-145', 'PLANEJAMENTO'), ('PA-195', 'ADICIONADO_DURANTE')]],
 'defeitos': [dict(id_defeito='DF-024', id_item_defeito='PA-196', id_item_origem='PA-138', severidade='BAIXA', ambiente_detectado='PRODUCAO', data_abertura='2026-11-05')],
 'impedimentos': [dict(id_impedimento='IP-007', id_item='PA-190', data_abertura='2026-11-05', data_fechamento='2026-11-10', tipo_impedimento='DEFINICAO_PENDENTE', dias_uteis_bloqueado='3', id_pessoa='P15'),
                  dict(id_impedimento='IP-008', id_item='PA-141', data_abertura='2026-11-09', tipo_impedimento='DEPENDENCIA_EXTERNA', id_pessoa='P15'),
                  dict(id_impedimento='IP-009', id_item='PA-142', data_abertura='2026-11-11', tipo_impedimento='AGUARDANDO_OUTRO_TIME', id_pessoa='P16')],
 'implantacoes': [dict(id_implantacao=a, data=b, id_sprint='S14', ambiente=c, versao=d, itens_implantados=e, tempo_ate_producao_h=f, falhou=g, **({'tempo_restauracao_h': h} if h else {}))
                  for a, b, c, d, e, f, g, h in [('IMP-054', '2026-11-03', 'PRODUCAO', '1.54', '2', '42.5', '1', '5.7'), ('IMP-055', '2026-11-04', 'HOMOLOGACAO', '1.55', '4', '19.4', '0', ''),
                    ('IMP-056', '2026-11-11', 'HOMOLOGACAO', '1.56', '3', '19.2', '0', ''), ('IMP-057', '2026-11-12', 'HOMOLOGACAO', '1.57', '1', '33.2', '0', ''),
                    ('IMP-058', '2026-11-12', 'PRODUCAO', '1.58', '3', '45.0', '1', '7.2'), ('IMP-059', '2026-11-13', 'HOMOLOGACAO', '1.59', '1', '43.8', '0', '')]],
 'mudancas': [dict(id_mudanca='SM-014', data_abertura='2026-11-11', id_solicitante='PI13', descricao='Adicionar sistema de visão para inspeção na linha', tipo_mudanca='ESCOPO', frente='PREDITIVA', id_atividade='A40', impacto_custo_rs='264200', impacto_prazo_du='10', impacto_pontos='0', status='EM_ANALISE'),
              dict(id_mudanca='SM-013', data_abertura='2026-10-19', id_solicitante='PI13', descricao='Integrar o sistema ao aplicativo corporativo', tipo_mudanca='ESCOPO', frente='AGIL', impacto_custo_rs='24100', impacto_prazo_du='0', impacto_pontos='8', status='REJEITADA', data_decisao='2026-11-10', nivel_decisor='GERENTE')],
 'reunioes': [dict(id_reuniao=a, data=b, tipo_reuniao=c, duracao_min=d, convidados=e, presentes=f, patrocinador_presente='0', decisoes_tomadas=g, pendencias_abertas=h, ata_publicada='1')
              for a, b, c, d, e, f, g, h in [('RE-086', '2026-11-03', 'PLANEJAMENTO_DA_SPRINT', '120', '5', '5', '1', '0'), ('RE-087', '2026-11-03', 'STATUS_SEMANAL', '60', '11', '9', '2', '3'),
                ('RE-088', '2026-11-10', 'STATUS_SEMANAL', '60', '7', '6', '2', '5'), ('RE-089', '2026-11-12', 'COMITE_DIRETOR', '120', '7', '4', '1', '5'),
                ('RE-090', '2026-11-13', 'RETROSPECTIVA', '60', '5', '4', '3', '0'), ('RE-091', '2026-11-13', 'REVISAO_DA_SPRINT', '60', '11', '6', '0', '3')]],
 'engajamento': [dict(mes='2026-11-01', id_parte=p, nivel_engajamento=n, satisfacao=s, interacoes_no_mes=i) for p, n, s, i in [
     ('PI01', 'NEUTRO', '5.9', '3'), ('PI02', 'APOIA', '8.4', '5'), ('PI03', 'APOIA', '7.8', '3'), ('PI04', 'APOIA', '7.4', '4'), ('PI05', 'APOIA', '7.1', '4'), ('PI06', 'APOIA', '6.7', '3'),
     ('PI07', 'APOIA', '7.9', '5'), ('PI08', 'APOIA', '8.2', '4'), ('PI09', 'APOIA', '8.1', '4'), ('PI10', 'APOIA', '7.4', '3'), ('PI11', 'NEUTRO', '6.2', '3'), ('PI12', 'NEUTRO', '5.8', '5'),
     ('PI13', 'RESISTENTE', '2.8', '1'), ('PI14', 'APOIA', '8.1', '5')]],
 'pulso': [dict(id_sprint='S14', satisfacao_media='4.00', respostas='5')],
 'okr': [dict(id_resultado_chave=k, data_medicao=d, valor=v) for k, v1, v2 in [('KR1', '8.7', '8.7'), ('KR2', '83.2', '84.9'), ('KR3', '271', '284'), ('KR4', '94.6', '93.5'), ('KR5', '41.7', '61.4'), ('KR6', '61.3', '77.3')]
         for d, v in [('2026-10-31', v1), ('2026-11-13', v2)]],
 'producao': [dict(semana_fim=s, id_atividade=a, quantidade_executada=q, hh_trabalhadas=h, efetivo_medio=e) for s, a, q, h, e in [
     ('2026-11-06', 'A33', '1066', '208', '6.5'), ('2026-11-13', 'A33', '1355', '252', '6.3'), ('2026-11-06', 'A35', '17', '166', '5.2'),
     ('2026-11-13', 'A35', '4', '38', '4.7'), ('2026-11-06', 'A39', '7', '330', '10.3'), ('2026-11-13', 'A39', '3', '165', '10.3')]],
 'funil': [dict(semana_inicio='2026-11-02', alcance='102', cadastros='2', ativados='0', ativos_na_semana='6', retidos_4_semanas='2', receita_rs='0', indicacoes='0', nps='35', chamados_suporte='20'),
           dict(semana_inicio='2026-11-09', alcance='102', cadastros='4', ativados='1', ativos_na_semana='5', retidos_4_semanas='3', receita_rs='0', indicacoes='0', nps='28', chamados_suporte='30')],
}
# B6 · movimentos do quadro, na ordem do boletim: (data, item, para, quem, revisão por par)
MOV = [('2026-11-03', 'PA-186', 'EM_REVISAO', 'P15', '0'), ('2026-11-03', 'PA-194', 'EM_ANDAMENTO', 'P16', None), ('2026-11-03', 'PA-194', 'EM_REVISAO', 'P16', '0'),
       ('2026-11-03', 'PA-186', 'EM_TESTE', 'P15', None), ('2026-11-03', 'PA-194', 'EM_TESTE', 'P16', None), ('2026-11-03', 'PA-192', 'EM_ANDAMENTO', 'P17', None),
       ('2026-11-04', 'PA-192', 'EM_REVISAO', 'P15', '1'), ('2026-11-04', 'PA-195', 'EM_ANDAMENTO', 'P16', None), ('2026-11-04', 'PA-192', 'EM_TESTE', 'P15', None),
       ('2026-11-04', 'PA-140', 'CONCLUIDO', 'P17', None), ('2026-11-04', 'PA-185', 'CONCLUIDO', 'P17', None), ('2026-11-05', 'PA-190', 'EM_ANDAMENTO', 'P15', None),
       ('2026-11-05', 'PA-195', 'EM_REVISAO', 'P16', '1'), ('2026-11-05', 'PA-188', 'CONCLUIDO', 'P17', None), ('2026-11-06', 'PA-141', 'EM_ANDAMENTO', 'P15', None),
       ('2026-11-06', 'PA-142', 'EM_ANDAMENTO', 'P16', None), ('2026-11-06', 'PA-195', 'EM_TESTE', 'P16', None), ('2026-11-06', 'PA-186', 'EM_ANDAMENTO', 'P17', None),
       ('2026-11-06', 'PA-194', 'EM_ANDAMENTO', 'P17', None), ('2026-11-06', 'PA-192', 'CONCLUIDO', 'P17', None), ('2026-11-09', 'PA-195', 'CONCLUIDO', 'P17', None),
       ('2026-11-10', 'PA-190', 'EM_REVISAO', 'P15', '0'), ('2026-11-10', 'PA-190', 'EM_TESTE', 'P15', None), ('2026-11-10', 'PA-190', 'CONCLUIDO', 'P17', None),
       ('2026-11-11', 'PA-186', 'EM_REVISAO', 'P15', '0'), ('2026-11-11', 'PA-186', 'EM_TESTE', 'P15', None), ('2026-11-11', 'PA-186', 'CONCLUIDO', 'P17', None),
       ('2026-11-12', 'PA-194', 'EM_REVISAO', 'P15', '0'), ('2026-11-12', 'PA-143', 'EM_ANDAMENTO', 'P16', None), ('2026-11-12', 'PA-194', 'EM_TESTE', 'P15', None),
       ('2026-11-12', 'PA-194', 'CONCLUIDO', 'P17', None), ('2026-11-13', 'PA-144', 'EM_ANDAMENTO', 'P15', None)]

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
