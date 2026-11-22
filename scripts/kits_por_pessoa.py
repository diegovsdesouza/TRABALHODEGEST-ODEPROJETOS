"""Gera o kit individual de cada integrante (HTML -> PDF): o que é dele, especificação de cada documento,
enunciado e dados da folha manuscrita, boletins que ele lança, apresentação e perguntas de arguição.

Uso: python scripts/kits_por_pessoa.py "<dossiê .docx>" docs/kits
"""
import os, re, sys, html, subprocess
import docx
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'testes'))
import roteiro_lancamento as R  # reaproveita tabelas e avisos dos boletins (gera docs/roteiro ao importar? não: só se chamado)

dossie, saida = sys.argv[1], sys.argv[2]
os.makedirs(saida, exist_ok=True)
D = docx.Document(dossie)
E = lambda s: html.escape(str(s))

def tab_docx(i):
    t = D.tables[i]; rows = [[c.text.replace('​', '') for c in r.cells] for r in t.rows]
    th = ''.join(f'<th>{E(c)}</th>' for c in rows[0])
    return '<table>' + f'<tr>{th}</tr>' + ''.join('<tr>' + ''.join(f'<td>{E(c)}</td>' for c in r) + '</tr>' for r in rows[1:]) + '</table>'

par = [p.text for p in D.paragraphs]
def texto_folha(m):
    i = next(k for k, t in enumerate(par) if t.startswith(m + ' —'))
    j = next(k for k in range(i + 1, len(par)) if re.match(r'^M\d —|^3\. ', par[k]))
    return f'<p class="enun"><b>{E(par[i])}</b></p>' + ''.join(f'<p class="enun">{E(t)}</p>' for t in par[i + 1:j] if t.strip())

FOLHAS = {'M1': [5], 'M2': [5], 'M3': [6, 7], 'M4': [8], 'M5': [9], 'M6': [10, 1], 'M7': [11, 12], 'M8': [13, 14, 15, 16]}

# ---------------- especificação dos documentos (enunciado + dados do G7)
DOC = {
 'D1': ('Termo de abertura e caso de negócio', [
   'Termo de abertura: objetivo aprovado ("aprovar as peças no cliente e iniciar o fornecimento em série na data contratual, com refugo de pintura abaixo de 6% na partida"), justificativa, escopo macro (as duas frentes), fora do escopo, patrocinador (Ramon Jesus, diretor de operações), gerente (P01 Leandro).',
   'Marcos (tabela 10) com as datas da linha de base: M1 projeto executivo 27/04/2026, M2 injetora na fábrica 19/11/2026, M3 Release 1 10/07/2026, M4 montagem concluída 31/12/2026, M5 SAT 16/03/2027, M6 aceite final 27/04/2027. Término contratual: 07/05/2027.',
   'Orçamento: ONT R$ 39.009.276 (preditiva R$ 38.271.476 + ágil R$ 737.800), contingência R$ 831.000, reserva gerencial R$ 1.170.000. Premissas, restrições (não parar a Linha de painéis; multa contratual) e critérios de sucesso.',
   'Caso de negócio (tabela 02): fluxo de caixa dos anos 0 a 7, VPL com TMA de 14% a.a., payback simples com interpolação (convenção 16). Diga se o projeto se paga e em quanto tempo.',
   'Fontes: tabelas 01, 02, 03 e 10 + ficha do projeto do dossiê.']),
 'D2': ('Partes interessadas e comunicação', [
   'Registro das 14 partes (tabela 03) com poder, interesse, engajamento inicial → desejado e expectativa.',
   'Matriz poder × interesse (alto = 4 ou 5) com a estratégia de cada quadrante (gerenciar de perto, manter satisfeito, manter informado, monitorar). É a mesma matriz da folha M6.',
   'Evolução do engajamento mês a mês (tabela 34, incluindo novembro do boletim B9). Destaques: PI13 (engenharia da montadora) está RESISTENTE com satisfação 2,8, e o patrocinador PI01 caiu de LIDERA para NEUTRO (5,9). Proponha ação para cada um.',
   'Plano de comunicação: reuniões (tabela 33) com frequência, quem participa, presença média, atas publicadas, decisões e pendências. Mostre a presença do patrocinador nas reuniões.',
   'Fontes: tabelas 03, 33 e 34.']),
 'D3': ('EAP e dicionário da EAP', [
   'EAP até o pacote de trabalho (tabela 06: 1 projeto, 8 entregas, 22 pacotes). Pacotes são entregas (substantivos); atividades começam com verbo no infinitivo.',
   'Dicionário da EAP: para cada pacote, descrição, responsável (tabela 04), atividades (tabela 07), orçamento (tabela 09) e critério de aceite.',
   'Regra dos 100%: a soma do orçamento dos pacotes = ONT da preditiva (R$ 38.271.476). Mostre a conferência.',
   'Fontes: tabelas 04, 06, 07 e 09. A EAP é a mesma das tarefas-resumo do ProjectLibre (D4).']),
 'D4': ('Cronograma no ProjectLibre', [
   'Entregas: arquivo .pod + PDF do Gantt + rede com o caminho crítico, na pasta docs/.',
   'Passos do enunciado: (1) calendário com os feriados da tabela 11; (2) EAP como tarefas-resumo e atividades dentro; (3) duração pela estimativa de três pontos, ⌈(O + 4M + P) ÷ 6⌉; (4) predecessoras com tipo (TI = FS, II = SS) e defasagem; (5) linha de base salva; (6) avanço real na data de status (13/11).',
   'Conferência obrigatória: o mesmo caminho crítico no ProjectLibre, no sistema e no papel. Linha de base: término em 27/04/2027 (du 304); caminho crítico A01 → A07 → A08 → A09 → A11 → A12 → A13 → A38 → A41 → A43 → A44 → A46 → A47 → A49 → A56. Previsão em 13/11: 10/05/2027.',
   'Atenção: no ProjectLibre a regra TI soma 1 dia automaticamente (o início é no dia útil seguinte), igual à convenção 2. Confira 3 ou 4 atividades contra o sistema (menu Prazo).',
   'Eu (Claude) gero um arquivo de importação com as 59 atividades, durações e ligações, para não digitar tudo.']),
 'D5': ('Orçamento, curva S e reservas', [
   'Orçamento por entrega da EAP e por categoria de custo (tabela 09). ONT do projeto R$ 39.009.276.',
   'Curva S: VP acumulado no fim de cada mês (convenção 4), com VA e CR até a data de status. A curva do dossiê em 25/09 (VP 32.721,8; VA 30.395,7; CR 30.119,3, em R$ mil) é o ponto de conferência.',
   'Reservas: contingência R$ 831.000 (riscos identificados, autoridade do gerente) e gerencial R$ 1.170.000 (não identificados, patrocinador). Linha de base de custo + reservas + gestão (R$ 85.800/mês de indiretos) = orçamento total, que deve fechar com o investimento do ano 0 do caso de negócio (R$ 43.007 mil).',
   'Fontes: tabelas 01, 02, 09 e 15. O sistema mostra a curva S no Dashboard e em Valor agregado.']),
 'D6': ('Matriz RACI e histograma', [
   'RACI: entregas da EAP × pessoas da equipe (tabela 04) e partes-chave (patrocinador, qualidade, fornecedores). Um único A por linha; o responsável do pacote (tabela 06) é o R.',
   'Histograma de horas planejadas por mês (tabela 40), total e por pessoa, comparado às horas apontadas (tabela 18). Destaque a superalocação de P06 em março/2026 (207,9 h planejadas para 176 h de capacidade).',
   'Fontes: tabelas 04, 06, 18 e 40 (convenção 18).']),
 'D7': ('Backlog e releases no Jira', [
   'Entregas: link do projeto Jira (Scrum) com o professor convidado e capturas dos relatórios.',
   'No Jira: versões R1, R2 e R3; os 5 épicos; backlog importado do CSV com pontos e prioridade (MoSCoW); a sprint da quinzena (S14) executada no quadro, na ordem do boletim B6; sprints futuras planejadas com a velocidade real (16 pontos por sprint); relatórios de burndown e de velocidade.',
   'No documento: plano de releases (R1 entregue em 07/08/2026, planejada para 10/07; previsão R2 em 11/12/2026, planejada para 02/10; R3 em 05/02/2027, planejada para 25/12/2026), MVP e a regra de previsão (convenção 10).',
   'Eu (Claude) gero o CSV do backlog pronto para importar.']),
 'D8': ('Rotina ágil e métricas', [
   'Cerimônias (tabela 33): planejamento, revisão, retrospectiva e status, com frequência e presença.',
   'Métricas: velocidade por sprint e média das 5 últimas (16,0 pt), burndown, tempo de ciclo, vazão, Lei de Little (M5), defeitos (tabela 24), impedimentos (tabela 22), pulso da equipe (tabela 35), métricas DORA (tabela 23, convenção 13) e funil do piloto (tabela 37).',
   'Leitura: o que essas métricas dizem sobre a Release 2, que trava o teste de aceite em campo.',
   'O sistema mostra tudo isso no Painel ágil.']),
 'D9': ('Riscos e reservas', [
   'Registro de riscos (tabela 26): causa, risco, efeito, probabilidade, impacto em custo e prazo, resposta, dono, status.',
   'Valor monetário esperado (convenção 12) das ameaças abertas e exposição total, comparada com a contingência de R$ 831.000. Matriz probabilidade × impacto 5 × 5 (é a folha M6).',
   'Ocorrências (tabela 27): quanto já se materializou (ex.: R15 câmbio, R$ 812 mil) e quanto da reserva foi consumido. A reserva cobre o que ainda está aberto?',
   'Respostas recomendadas para os 5 maiores riscos, com dono e custo da resposta.']),
 'D10': ('Aquisições e qualidade', [
   'Contratos (tabela 30): tipo de contrato de cada fornecedor e por que ele faz sentido; medições previstas × pagas (tabela 31). Desvios: CT03 injetora (câmbio, +R$ 812 mil) e CT07 obra civil (medição acima do previsto em todas as medições, +R$ 291 mil).',
   'Multas por atraso (convenção 14) dos contratos atrasados.',
   'Seleção do fornecedor de comissionamento elétrico (tabela 32): nota ponderada pela convenção 15 (preço 35%, técnica 30%, prazo 15%, experiência 10%, garantia 10%) e recomendação.',
   'Qualidade: inspeções e testes de aceite (tabela 25) por fornecedor, não conformidades, reprovações e custo de retrabalho; defeitos da trilha ágil (tabela 24).']),
 'D11': ('Mudanças e Bússola de Abordagem', [
   'Registro de mudanças (tabela 28 + boletim B8): cada solicitação com impacto, decisão e quem decidiu, conferindo a matriz de alçadas (tabela 05). SM-014 (sistema de visão, R$ 264 mil e 10 du) está em análise e passa do limite do gerente.',
   'Escopo que entrou sem controle: 8 itens PEDIDO_DIRETO da montadora (PI13), 22 pontos, inclusive o PA-195 na S14, sem solicitação de mudança.',
   'Bússola de Abordagem: para cada domínio (escopo, mudança, entrega, usuário), qual trilha usar e a variável que decide (escopo estável × incerto; mudança cara × barata; entrega de uma vez × em partes; usuário longe × perto).',
   'Mapa de interfaces: onde uma trilha depende da outra (Release 2 → SAT A47; Release 3 → aceite final A56) e quem responde por cada ponto de encontro.']),
 'D12': ('Estratégia do projeto', [
   'Duas a três páginas: por que o projeto é híbrido, como as trilhas se encontram e o que define o término hoje (a cadeia da injetora, A12 → … → A56).',
   'Estratégia de prazo: comprimir (folha M4: 5 dias ao menor custo × R$ 50.100 por dia de atraso), reforçar a equipe ágil (C2) ou aceitar o atraso.',
   'Governança e rotina de controle: quem decide o quê (alçadas), frequência de status, indicadores acompanhados.']),
 'D13': ('Pessoal e custos de pessoal', [
   'Custo de cada pessoa (tabela 39, convenção 17): remuneração × (1 + encargos) + benefícios = custo mensal; ÷ 168 h = custo/hora (confere com a tabela 04). Folha mensal: R$ 282.910,40.',
   'Alocação planejada × apontada por mês (tabelas 40 e 18, convenção 18): quem está sobrecarregado e quem está abaixo do plano (desvio acima de 20%).',
   'Trilha ágil: pontos por hora de cada desenvolvedor e custo por ponto (convenção 20).',
   'Impacto do reajuste salarial previsto (convenção 19) até o término previsto.']),
 'D14': ('Produtividade das equipes', [
   'Para cada atividade da tabela 41 com produção na tabela 42 (convenção 20): produtividade real (quantidade ÷ Hh), índice de produtividade (real ÷ planejada), índice de efetivo (efetivo médio ÷ equipe planejada) e duração restante.',
   'Diagnóstico por fornecedor: falta gente ou falta rendimento? Destaque A33 (elétrica, 47 du atrasada) e A39 (cabine de pintura), que também estão na folha M8.']),
 'D15': ('Análise financeira', [
   'Fluxo de caixa ano a ano (tabela 02) e VPL a 14% a.a., payback simples (convenção 16).',
   'Estimativa no término (ENT = ONT ÷ IDC): R$ 41,76 mi em 13/11 (desvio de R$ 2,75 mi sobre o ONT) e de onde vem o desvio (por entrega: obra civil e elétrica com IDC abaixo de 1).',
   'Custo de cada dia de atraso: R$ 50.100 por dia útil além de 07/05/2027. Hoje: 1 du, R$ 50.100.',
   'Efeito do atraso e do custo no VPL (convenção 23): é a base que o Diego usa no D16.']),
 'D16': ('Cenários e decisão', [
   'Os 6 cenários (tabelas 43 a 46) calculados: novo término (convenção 21), custo (22), VPL e resultado = VPL − custo do atraso (23), e o que se perde ao escolher cada um.',
   'Pelo menos uma combinação testada (a coluna combinavel_com da tabela 43 diz quais são possíveis).',
   'Recomendação ao comitê, com a decisão, o dono e o prazo. Conferência: C1, C3 e C4 batem com a tabela do dossiê (folha M7).',
   'O simulador de cenários do sistema (R16) faz as contas; o documento traz a comparação e a decisão.']),
 'D17': ('Modelo 3D', [
   'Modelo 3D da obra (tabela 38: posição e volume de cada elemento), com formas reconhecíveis, montado em etapas ligadas às atividades, com controle de data mostrando a linha subindo até ficar pronta.',
   'No sistema (R12) e em docs/ (capturas das etapas). Eu (Claude) construo o modelo no sistema; você define a ordem de implantação (campo ordem_de_implantacao, hoje vazio) e explica na apresentação.']),
 'REL': ('Relatório gerencial e apresentação', [
   'Até 15 slides, em PDF. A conclusão vem antes da análise.',
   'Diagnóstico: prazo, custo, escopo, qualidade, riscos, contratos e pessoas. Pelo menos 6 achados, cada um com evidência, causa, impacto em reais ou dias, ação e dono. Achado sem número não conta.',
   'Decisão: os 6 cenários, a combinação testada e a recomendação.',
   'Apresentação de 25 min: 12 de apresentação (todos falam), 4 de boletim surpresa ao vivo e 9 de arguição individual. Caderno em papel na mesa.']),
}

PERG = {
 'Diego': [('Por que vocês recomendam esse cenário e não o C1?', 'Compare o resultado (VPL − custo do atraso) de cada um e diga o que se perde ao escolher.'),
           ('Como a combinação testada foi calculada?', 'Mostre no simulador quais mudanças da rede, do backlog e da equipe entram juntas e o novo término.')],
 'Caique': [('O que define a data de término hoje?', 'A cadeia da injetora: A12 (transporte, 70%) atrasou 9 du e empurra A13 → A38 → … → A56; término previsto em 10/05/2027, 1 du além do contrato.'),
            ('Por que o A33 é crítico na sub-rede da M1, se está ligado ao A32 por II+15?', 'Porque o A34 precisa do término dos dois, e o A33 termina depois (du 44 contra 42).')],
 'José': [('De onde vem o desvio de custo?', 'IDC abaixo de 1 na obra civil e na elétrica e o câmbio da injetora (R15, R$ 812 mil); ENT R$ 41,76 mi contra ONT R$ 39,01 mi.'),
          ('O que o IDPT diz?', 'Quanto o desempenho de custo precisa melhorar no restante para terminar dentro do ONT; acima de 1 é difícil de atingir.')],
 'Marjorie': [('A contingência cobre os riscos?', 'Compare a exposição (soma do VME das ameaças abertas) com R$ 831 mil e diga quanto já foi consumido por ocorrências.'),
              ('Por que comprimir não é sempre bom?', 'Cada dia comprimido custa mais que o anterior; compare com R$ 50.100 por dia de atraso (M4).')],
 'Guilherme': [('Como vocês previram a Release 2?', 'Pontos restantes das releases 1 e 2 ÷ velocidade média das 5 últimas sprints (16 pt), arredondado para cima: 2 sprints, fim da S16 (11/12/2026).'),
               ('O que é escopo sem controle aqui?', 'Os 8 pedidos diretos da montadora (22 pontos) que entraram no backlog sem solicitação de mudança.')],
 'Arley': [('Falta gente ou falta produtividade no A33?', 'Compare o índice de efetivo com o índice de produtividade (convenção 20) e diga qual dos dois explica o atraso.'),
           ('Quem está sobrecarregado?', 'Mostre o desvio de alocação acima de 20% (planejado × apontado) e o caso de P06 em março.')],
}

PESSOAS = [
 ('Diego', 'Coordenação', ['D16', 'REL'], ['M7'], 'GitHub', ['sprint', 'backlog', 'itemSprint', 'defeitos', 'quadro', 'impedimentos', 'implantacoes'], 'Abertura, cenários e recomendação',
  ['Convidar os colegas e o professor como colaboradores no GitHub e mandar o link do sistema e o roteiro ao grupo.',
   'Você lança a trilha ágil (B5 a B7): faça "Novo item no backlog" ANTES de "Itens da sprint" e do quadro, e mova os cartões na ordem exata. É o treino para o boletim surpresa ao vivo.',
   'Depois dos lançamentos, abrir Conferência e checar as 13 linhas "até 13/11" (todas ✔).',
   'Montar a ficha do grupo (uma página: quem fez o quê), o diário de prompts (10 entradas, de 3 pessoas) e enviar o formulário de entrega até 24/11, 23h59.']),
 ('Caique', '', ['D3', 'D4', 'D12', 'D17'], ['M1', 'M2'], 'ProjectLibre', ['avanco', 'producao'], 'Prazo, caminho crítico e modelo 3D',
  ['Instalar o ProjectLibre e importar o arquivo que eu gero; salvar a linha de base e o avanço em 13/11; exportar o PDF do Gantt.']),
 ('José', '', ['D1', 'D5', 'D15'], ['M3'], '—', [R.H1, 'custos'], 'Custo, valor agregado e caso de negócio', []),
 ('Marjorie', '', ['D9', 'D10'], ['M4', 'M6'], '—', [R.H2, 'medicoes', 'inspecoes'], 'Riscos, reserva e fornecedores', []),
 ('Guilherme', '', ['D7', 'D8', 'D11'], ['M5'], 'Jira (responsável)', ['mudancas', 'okr', 'funil'],
  'Trilha ágil, escopo e Bússola de Abordagem',
  ['Criar o site gratuito do Jira e o projeto Scrum; convidar o professor; importar o CSV do backlog que eu gero; criar as versões R1, R2 e R3; executar a S14 no quadro na ordem do boletim B6; capturar burndown e velocidade.']),
 ('Arley', '', ['D2', 'D6', 'D13', 'D14'], ['M8'], '—', ['reunioes', 'engajamento', 'pulso'], 'Partes interessadas e pessoas', []),
]

CSS = '''@page { size: A4; margin: 12mm; } body { font-family: "DejaVu Sans", Arial, sans-serif; font-size: 10.5px; color: #1d2733; line-height: 1.4; }
h1 { font-size: 20px; color: #1f3a5f; margin: 0; } .sub { color: #6b7785; margin: 2px 0 10px; }
h2 { font-size: 14px; color: #fff; background: #1f3a5f; padding: 4px 8px; margin: 14px 0 6px; } h3 { font-size: 12px; color: #1f3a5f; margin: 10px 0 4px; }
table { border-collapse: collapse; width: 100%; margin: 4px 0 6px; } th { background: #e8eef5; } th, td { border: 1px solid #c9d2dc; padding: 3px 4px; text-align: left; vertical-align: top; }
ul { margin: 2px 0 4px 16px; padding: 0; } li { margin: 2px 0; } .chip { background: #1f3a5f; color: #fff; border-radius: 8px; padding: 0 6px; font-size: 10px; }
.dica { background: #fff4e5; border: 1px solid #ffc58b; padding: 4px 6px; margin: 3px 0; } .enun { margin: 3px 0; } .quebra { page-break-before: always; }
td.n { color: #6b7785; width: 16px; } .resumo td:first-child { width: 22%; font-weight: bold; background: #f3f6f9; }'''

def kit(nome, papel, docs, folhas, ferr, telas, apres, tarefas):
    resumo = f'''<table class="resumo"><tr><td>Documentos</td><td>{", ".join(f"{d} {DOC[d][0]}" if d != "REL" else "Relatório gerencial (slides)" for d in docs)}</td></tr>
      <tr><td>Folha(s) à mão</td><td>{", ".join(folhas)} · A4 quadriculado, caneta, com nome e assinatura</td></tr><tr><td>Ferramenta</td><td>{ferr}</td></tr>
      <tr><td>Lança no sistema</td><td>{", ".join((lambda k, ls, c: f"{R.BOL[k]} {R.TIT[k]}" + (f" ({c})" if c else "") if k != "quadro" else "B6 Quadro da sprint")(*R.item(t)) for t in telas)}</td></tr>
      <tr><td>Apresenta</td><td>{apres}</td></tr></table>'''
    extra = ''.join(f'<li>{E(t)}</li>' for t in tarefas)
    docs_html = ''.join(f'<h3>{d if d != "REL" else ""} {E(DOC[d][0])}</h3><ul>' + ''.join(f'<li>{E(x)}</li>' for x in DOC[d][1]) + '</ul>' for d in docs)
    folhas_html = ''.join(f'<h3>Folha {m}</h3>{texto_folha(m)}<p class="dica">Dados do dossiê para a folha {m}:</p>' + ''.join(tab_docx(i) for i in FOLHAS[m]) for m in folhas)
    bol = ''
    for t in telas:
        t, linhas, comp = R.item(t)
        if t == 'quadro': bol += f'<h3><span class="chip">B6</span> Quadro da sprint · {len(R.MOV)} movimentos</h3>{R.quadro()}'
        else: bol += f'<h3><span class="chip">{R.BOL[t]}</span> {E(R.TIT[t])}{" · " + comp if comp else ""} · {len(linhas)} linha(s)</h3>' + (f'<p class="dica">{R.AVISO[t]}</p>' if t in R.AVISO else '') + R.tabela(t, linhas)
    perg = ''.join(f'<li><b>{E(q)}</b><br>{E(a)}</li>' for q, a in PERG[nome])
    return f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>Kit {nome} · G7</title><style>{CSS}</style></head><body>
<h1>{nome}{(" · " + papel) if papel else ""}</h1><p class="sub">ENGN62 Gestão de Projetos · Trabalho final "Sala de Guerra das Duas Trilhas" · G7 Plásticos Abrantes</p>
{resumo}
<h2>Prazos e regras</h2><ul><li><b>Seg 23/11:</b> ponto de controle, com o sistema no ar · <b>Ter 24/11, 23h59:</b> entrega digital · <b>25/11 ou 30/11:</b> apresentação de 25 min.</li>
<li>Pelo menos <b>1 commit</b> no GitHub e <b>2 entradas</b> no diário de prompts (o que pediu à IA, o que ela errou e como você corrigiu).</li>
<li>Todo número com fonte (tabela e filtro) e unidade. Cálculo sem interpretação vale metade. Use as 23 convenções do DICIONARIO.md.</li>
<li>Sua folha é feita e assinada por você; confira com o gabarito que eu mando depois que você terminar. "Foi a IA que fez" não é resposta na arguição.</li>
<li>Sistema: <b>https://trabalhodegest-odeprojetos.netlify.app</b> · Repositório: github.com/diegovsdesouza/TRABALHODEGEST-ODEPROJETOS (comece toda conversa com a IA pelo CONTEXTO.md).</li>
{extra}</ul>
<h2>Especificação dos seus documentos</h2>{docs_html}
<h2 class="quebra">Sua folha manuscrita</h2>{folhas_html}
{f'<h2 class="quebra">Boletins que você lança no sistema</h2><p>Entre no sistema com a sua conta (Entrar → Criar conta), vá em Lançamentos e digite uma linha por vez, tocando em Salvar. Nunca lance a mesma linha duas vezes; se errar, apague na lista de baixo e lance de novo.</p>{bol}' if telas else ''}
<h2>Na apresentação e na arguição</h2><p>Você apresenta: <b>{apres}</b>. Perguntas prováveis:</p><ul>{perg}</ul>
</body></html>'''

for p in PESSOAS:
    nome = p[0]; arq = os.path.join(saida, f'kit-{nome.lower().replace("é", "e")}')
    open(arq + '.html', 'w').write(kit(*p))
    subprocess.run(['google-chrome', '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={arq}.pdf', arq + '.html'], capture_output=True)
    print(nome, arq + '.pdf')
