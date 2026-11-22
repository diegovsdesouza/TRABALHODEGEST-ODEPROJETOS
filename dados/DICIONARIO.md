# Dicionário de dados — Trabalho Final ENGN62 (2026.2)

Todas as tabelas existem em dois formatos: CSV (UTF-8, separador vírgula, decimal ponto, datas AAAA-MM-DD) na pasta `dados/` e como abas do arquivo `.xlsx` do grupo.
Chaves principais: `id_atividade`, `codigo_eap`, `id_item`, `id_epico`, `id_sprint`, `id_release`, `id_pessoa`, `id_parte`, `id_contrato`, `id_fornecedor`, `id_risco`, `id_mudanca`.
du = dias úteis (segunda a sexta, exceto feriados da tabela 11).

## Bloco A. Governança e contexto

### 01_projeto_parametros — Parâmetros do projeto

Dados gerais, datas de referência, reservas, taxas e pesos usados nos cálculos.

**Granularidade:** Uma linha por parâmetro

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `parametro` | texto | — | Nome do parâmetro | Chave única. Lista completa no fim deste dicionário |
| `valor` | texto ou número | ver unidade | Valor do parâmetro | Datas em AAAA-MM-DD; frações em decimal (0,15 = 15%) |
| `unidade` | texto | — | Unidade do valor | R$, data, fração, du, texto... |
| `descricao` | texto | — | Significado do parâmetro |  |

### 02_caso_de_negocio — Caso de negócio (fluxo anual)

Fluxo de caixa aprovado no caso de negócio, por ano. O ano 0 é o da implantação.

**Granularidade:** Uma linha por ano (0 a 7)

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `ano` | inteiro | ano | Ano do fluxo | 0 = implantação; 1 = primeiro ano de operação |
| `investimento_rs` | decimal | R$ | Desembolso de investimento no ano | No ano 0: orçamento das duas frentes + reservas + gestão. Valor positivo = saída de caixa |
| `beneficio_bruto_rs` | decimal | R$ | Ganho bruto gerado pelo projeto no ano | Margem adicional, custo evitado ou receita nova |
| `custo_operacional_rs` | decimal | R$ | Custo para operar o que o projeto entregou | Fluxo líquido do ano = benefício − custo operacional − investimento |

### 03_partes_interessadas — Registro de partes interessadas

Quem afeta ou é afetado pelo projeto, com poder, interesse e engajamento no início.

**Granularidade:** Uma linha por parte interessada

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_parte` | texto | — | Identificador da parte interessada | PI01, PI02... Chave usada nas tabelas 14, 28 e 34 |
| `parte_interessada` | texto | — | Cargo, área ou organização |  |
| `contato` | texto | — | Nome da pessoa de contato | Nome fictício |
| `papel_no_projeto` | texto | — | Relação com o projeto | Patrocinador, cliente interno, regulador, fornecedor... |
| `tipo` | categoria | — | Interna ou externa à empresa | INTERNO, EXTERNO |
| `poder` | inteiro | escala 1 a 5 | Capacidade de influenciar decisões do projeto | 1 = muito baixo; 5 = muito alto |
| `interesse` | inteiro | escala 1 a 5 | Quanto o resultado do projeto afeta a parte | 1 = muito baixo; 5 = muito alto |
| `engajamento_inicial` | categoria | — | Nível de engajamento no início do projeto | DESCONHECE, RESISTENTE, NEUTRO, APOIA, LIDERA |
| `engajamento_desejado` | categoria | — | Nível de engajamento necessário para o projeto dar certo | Mesmo domínio do campo anterior |
| `principal_expectativa` | texto | — | O que a parte espera do projeto |  |

### 04_equipe — Equipe do projeto

Pessoas alocadas, com papel, frente, custo por hora e período de permanência.

**Granularidade:** Uma linha por pessoa

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_pessoa` | texto | — | Identificador da pessoa | P01, P02... Chave usada nas tabelas 06, 07, 14, 17, 18, 21, 22 e 26 |
| `nome` | texto | — | Nome | Nome fictício |
| `papel` | texto | — | Função no projeto |  |
| `frente` | categoria | — | Frente em que atua | GESTAO, PREDITIVA, AGIL |
| `disciplina` | categoria | — | Disciplina pela qual responde (só frente preditiva) | Códigos de disciplina na tabela 07; vazio nas demais frentes |
| `senioridade` | categoria | — | Nível de experiência | JR, PL, SR |
| `vinculo` | categoria | — | Forma de contratação | CLT, PJ |
| `custo_hora_rs` | decimal | R$/h | Custo da hora normal com encargos | Hora extra custa custo_hora_rs × fator_hora_extra |
| `alocacao_pct` | inteiro | % | Parcela da jornada dedicada ao projeto | 100 = dedicação integral |
| `data_entrada` | data | — | Primeiro dia no projeto |  |
| `data_saida` | data | — | Último dia no projeto | Vazio = continua no projeto |

### 05_matriz_alcadas — Matriz de alçadas

Quem pode aprovar mudanças, por valor e por prazo.

**Granularidade:** Uma linha por nível decisor

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `nivel_decisor` | categoria | — | Nível que decide | GERENTE, PATROCINADOR, COMITE |
| `limite_custo_rs` | decimal | R$ | Maior impacto de custo que o nível pode aprovar | Vazio = sem limite |
| `limite_prazo_du` | inteiro | du | Maior impacto de prazo que o nível pode aprovar | Vazio = sem limite |
| `pode_alterar_escopo` | categoria | — | Se o nível pode aprovar mudança de escopo | SIM, NAO |
| `descricao` | texto | — | Resumo da alçada |  |

## Bloco B. Plano da trilha preditiva

### 06_eap — Estrutura analítica do projeto (EAP)

Decomposição do trabalho em entregas e pacotes de trabalho, com responsável e critério de aceite.

**Granularidade:** Uma linha por elemento da EAP

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `codigo_eap` | texto | — | Código hierárquico do elemento | 1 = projeto; 1.x = entrega; 1.x.y = pacote de trabalho |
| `nome` | texto | — | Nome do elemento | Substantivo, não verbo |
| `nivel` | inteiro | — | Nível na hierarquia | 1, 2 ou 3 |
| `codigo_pai` | texto | — | Código do elemento imediatamente acima | Vazio no nível 1 |
| `tipo_elemento` | categoria | — | Tipo do elemento | PROJETO, ENTREGA, PACOTE_DE_TRABALHO |
| `disciplina` | categoria | — | Disciplina do pacote | Vazio nos níveis 1 e 2 |
| `id_responsavel` | texto | — | Pessoa responsável pelo elemento | Chave da tabela 04 |
| `criterio_de_aceite` | texto | — | Condição para o pacote ser aceito | Só nos pacotes de trabalho |

### 07_atividades — Atividades

Atividades da trilha preditiva, com estimativa de três pontos, e os três marcos que representam a frente ágil na rede.

**Granularidade:** Uma linha por atividade

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_atividade` | texto | — | Identificador da atividade | A01, A02... Chave usada nas tabelas 08, 09, 10, 12, 17, 18, 19, 25, 26, 27, 28, 31 e 38 |
| `codigo_eap` | texto | — | Pacote de trabalho a que pertence | Chave da tabela 06 |
| `nome_atividade` | texto | — | Descrição da atividade |  |
| `disciplina` | categoria | — | Disciplina | LINHA: ENG, REG, SUP, CIV, ELE, AUT, MEC, COM, TRE. DIGITAL: PRD, INF, REG, INT, HW, CON, OPS, QA. AGI = frente ágil |
| `tipo_atividade` | categoria | — | Como a duração é definida | ESTIMADA (três pontos) ou MARCO_AGIL (duração fixa, igual ao calendário das sprints) |
| `duracao_otimista_du` | inteiro | du | Duração no melhor caso (O) | Vazio nos marcos ágeis |
| `duracao_mais_provavel_du` | inteiro | du | Duração mais provável (M) | Vazio nos marcos ágeis |
| `duracao_pessimista_du` | inteiro | du | Duração no pior caso (P) | Vazio nos marcos ágeis |
| `duracao_fixa_du` | inteiro | du | Duração dos marcos ágeis na linha de base | Dias úteis das sprints planejadas até a release; vazio nas atividades estimadas |
| `id_responsavel` | texto | — | Pessoa responsável | Chave da tabela 04 |
| `horas_internas_orcadas` | decimal | h | Horas da equipe própria previstas para a atividade | Base do orçamento de PESSOAL_INTERNO |

### 08_dependencias — Dependências entre atividades

Ligações da rede de precedência.

**Granularidade:** Uma linha por ligação

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_predecessora` | texto | — | Atividade que vem antes | Chave da tabela 07 |
| `id_sucessora` | texto | — | Atividade que depende da anterior | Chave da tabela 07 |
| `tipo_dependencia` | categoria | — | Tipo da ligação | TI = término → início; II = início → início |
| `defasagem_du` | inteiro | du | Espera mínima entre as duas atividades | TI: início ≥ término da predecessora + 1 + defasagem. II: início ≥ início da predecessora + defasagem |

### 09_orcamento_linha_de_base — Orçamento da linha de base

Custo orçado de cada atividade, por categoria. A soma é o orçamento no término (ONT) da frente preditiva.

**Granularidade:** Uma linha por atividade e categoria de custo

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_atividade` | texto | — | Atividade | Chave da tabela 07 |
| `categoria_custo` | categoria | — | Natureza do custo | PESSOAL_INTERNO, SERVICO_CONTRATADO, EQUIPAMENTO, MATERIAL, LICENCAS_E_NUVEM, OUTROS |
| `valor_orcado_rs` | decimal | R$ | Valor orçado | PESSOAL_INTERNO = horas_internas_orcadas × custo_hora_rs do responsável |
| `id_contrato` | texto | — | Contrato que cobre a linha, se houver | Chave da tabela 30; vazio = compra avulsa ou equipe própria |

### 10_marcos — Marcos do projeto

Marcos combinados com o patrocinador. A data da linha de base não é dada: sai da rede.

**Granularidade:** Uma linha por marco

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_marco` | texto | — | Identificador do marco | M1 a M6 |
| `nome_marco` | texto | — | Nome do marco |  |
| `id_atividade` | texto | — | Atividade cujo término define o marco | Chave da tabela 07 |
| `regra` | texto | — | Como a data do marco é obtida |  |
| `criterio_de_aceite` | texto | — | Condição para considerar o marco cumprido |  |
| `data_real` | data | — | Data em que o marco foi cumprido | Vazio = ainda não cumprido |

### 11_calendario — Calendário do projeto

Todos os dias do início do projeto até 2027, com dias úteis, feriados e a sprint de cada data.

**Granularidade:** Uma linha por dia corrido

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `data` | data | — | Dia |  |
| `dia_semana` | texto | — | Dia da semana |  |
| `dia_util` | inteiro | 0 ou 1 | Se é dia útil do projeto | 1 = segunda a sexta que não é feriado |
| `feriado` | texto | — | Nome do feriado | Vazio se não é feriado |
| `dia_util_projeto` | inteiro | du | Número do dia útil contado a partir do início do projeto | 1 = data_inicio_projeto; vazio em dias não úteis. Use para converter du em data |
| `id_sprint` | texto | — | Sprint que contém o dia | Chave da tabela 15; vazio fora das sprints e nos fins de semana |

### 12_compressao_opcoes — Opções de compressão

Quanto cada atividade pode ser encurtada e a que custo (reforço de equipe, hora extra, frete aéreo).

**Granularidade:** Uma linha por atividade compressível

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_atividade` | texto | — | Atividade | Chave da tabela 07. Atividade já concluída não pode mais ser comprimida |
| `duracao_normal_du` | inteiro | du | Duração da linha de base | Igual à duração calculada pela estimativa de três pontos |
| `duracao_minima_du` | inteiro | du | Menor duração possível |  |
| `custo_adicional_por_du_rs` | decimal | R$/du | Custo para reduzir um dia útil | Compare com custo_do_atraso_por_du_rs (tabela 01) |

## Bloco C. Plano da trilha ágil

### 13_epicos — Épicos

Grandes blocos de funcionalidade do produto digital.

**Granularidade:** Uma linha por épico

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_epico` | texto | — | Identificador do épico | EP01, EP02... Chave usada nas tabelas 14 e 38 |
| `nome_epico` | texto | — | Nome do épico |  |
| `persona` | texto | — | Usuário principal do épico |  |
| `beneficio_esperado` | texto | — | Resultado que o épico deve produzir para a persona |  |
| `id_release_planejada` | texto | — | Release em que o épico foi planejado | R1, R2, R3 (tabela 16) |
| `valor_de_negocio` | inteiro | escala 1 a 100 | Valor atribuído pelo patrocinador e pelo Product Owner | Quanto maior, mais valioso |

### 14_backlog_itens — Backlog do produto

Todos os itens do backlog, com a situação de cada um na data do arquivo.

**Granularidade:** Uma linha por item

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_item` | texto | — | Chave do item, no padrão do Jira | SIGLA-número. Chave usada nas tabelas 20, 21, 22 e 24 |
| `id_epico` | texto | — | Épico do item | Chave da tabela 13 |
| `tipo_item` | categoria | — | Tipo do item | HISTORIA, TECNICA (tarefa técnica), SPIKE (investigação), BUG (defeito) |
| `titulo` | texto | — | Resumo do item |  |
| `historia_de_usuario` | texto | — | Texto no formato Como / quero / para | Só nas histórias do plano inicial |
| `pontos` | inteiro | pontos de história | Estimativa relativa de esforço | 1, 2, 3, 5, 8 ou 13 |
| `prioridade_moscow` | categoria | — | Prioridade | MUST, SHOULD, COULD, WONT |
| `valor_de_negocio` | inteiro | escala 1 a 100 | Valor atribuído ao item |  |
| `ordem_no_backlog` | inteiro | posição | Posição do item na ordenação do Product Owner | 1 = topo |
| `id_release` | texto | — | Release a que o item pertence | R1, R2, R3 |
| `origem` | categoria | — | Como o item entrou no backlog | PLANO_INICIAL, MUDANCA_APROVADA, PEDIDO_DIRETO (sem solicitação de mudança), DEFEITO |
| `id_mudanca` | texto | — | Solicitação de mudança que criou o item | Chave da tabela 28; vazio nas demais origens |
| `id_solicitante` | texto | — | Parte interessada que pediu o item | Chave da tabela 03; preenchido em PEDIDO_DIRETO e MUDANCA_APROVADA |
| `data_criacao` | data | — | Data em que o item foi criado |  |
| `status` | categoria | — | Situação na data do arquivo | A_FAZER, EM_ANDAMENTO, EM_REVISAO, EM_TESTE, CONCLUIDO |
| `id_sprint_atual` | texto | — | Última sprint em que o item esteve | Chave da tabela 15; vazio se nunca entrou em sprint |
| `id_responsavel` | texto | — | Último desenvolvedor que trabalhou no item | Chave da tabela 04 |
| `revisao_por_par` | inteiro | 0 ou 1 | Se o código foi revisado por outra pessoa antes do teste | 1 = revisado; 0 = revisão pulada; vazio = ainda não saiu do desenvolvimento |
| `data_inicio` | data | — | Primeira entrada em EM_ANDAMENTO |  |
| `data_conclusao` | data | — | Data em que chegou a CONCLUIDO |  |

### 15_sprints — Sprints

Calendário e orçamento das sprints: as já realizadas e as planejadas na linha de base.

**Granularidade:** Uma linha por sprint

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_sprint` | texto | — | Identificador da sprint | S01, S02... |
| `numero` | inteiro | — | Número da sprint |  |
| `data_inicio` | data | — | Segunda-feira de início |  |
| `data_fim` | data | — | Sexta-feira de término |  |
| `dias_uteis` | inteiro | du | Dias úteis da sprint | Feriados reduzem a capacidade |
| `planejada_na_linha_de_base` | inteiro | 0 ou 1 | Se a sprint faz parte do plano aprovado | A soma do orçamento das sprints com 1 é o ONT da frente ágil |
| `id_release_alvo` | texto | — | Release em que a sprint trabalha, segundo o plano | R1, R2, R3 |
| `orcamento_sprint_rs` | decimal | R$ | Orçamento de uma sprint (time + nuvem e licenças) |  |
| `pessoas_dia_disponiveis` | inteiro | pessoas-dia | Dias de desenvolvedor disponíveis na sprint | Só nas sprints encerradas; desconta férias, saídas e feriados |
| `horas_extras_autorizadas` | categoria | — | Se a diretoria autorizou hora extra na sprint | SIM, NAO; vazio nas sprints futuras |
| `meta_da_sprint` | texto | — | Meta combinada no planejamento | Vazio nas sprints futuras |

### 16_releases — Releases

As três entregas do produto ao público.

**Granularidade:** Uma linha por release

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_release` | texto | — | Identificador | R1, R2, R3 |
| `nome_release` | texto | — | Nome |  |
| `id_sprint_planejada` | texto | — | Sprint em que a release deveria sair | Chave da tabela 15 |
| `data_planejada` | data | — | Data planejada (fim da sprint planejada) |  |
| `data_real` | data | — | Data em que a release entrou em produção | Vazio = ainda não entregue |
| `objetivo` | texto | — | Para que serve a release |  |

## Bloco D. Execução e controle

### 17_avanco_semanal — Avanço físico semanal (trilha preditiva)

Relatório semanal do responsável: avanço físico acumulado de cada atividade em andamento.

**Granularidade:** Uma linha por semana e atividade em execução

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `semana_fim` | data | — | Sexta-feira de fechamento da semana |  |
| `id_atividade` | texto | — | Atividade | Chave da tabela 07 |
| `avanco_acumulado_pct` | inteiro | % | Avanço físico acumulado informado pelo responsável | 0 a 100. Semana sem informe: vale o último valor informado |
| `situacao` | categoria | — | Situação da atividade na semana | EM_ANDAMENTO, CONCLUIDA |
| `data_inicio_real` | data | — | Data real de início |  |
| `data_termino_real` | data | — | Data real de término | Preenchida na semana em que a atividade chega a 100% |
| `id_responsavel` | texto | — | Quem informou | Chave da tabela 04 |

### 18_apontamento_horas — Apontamento de horas

Folha de horas semanal da equipe própria, por atividade, sprint ou gestão.

**Granularidade:** Uma linha por semana, pessoa e item

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `semana_inicio` | data | — | Segunda-feira da semana |  |
| `id_pessoa` | texto | — | Pessoa | Chave da tabela 04 |
| `tipo_item` | categoria | — | Onde as horas foram gastas | ATIVIDADE (trilha preditiva), SPRINT (frente ágil), GESTAO (gestão do projeto) |
| `id_item` | texto | — | Atividade, sprint ou GESTAO | Chave da tabela 07 ou 15, conforme tipo_item |
| `horas_normais` | decimal | h | Horas dentro da jornada |  |
| `horas_extras` | decimal | h | Horas além da jornada | Custam fator_hora_extra vezes a hora normal |

### 19_custos_realizados — Custos realizados

Notas, medições e despesas pagas. Não inclui o custo da equipe própria, que sai da tabela 18.

**Granularidade:** Uma linha por lançamento

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_lancamento` | texto | — | Identificador do lançamento | L00001... |
| `data` | data | — | Data do lançamento |  |
| `frente` | categoria | — | Frente que consumiu o recurso | PREDITIVA, AGIL, GESTAO |
| `categoria_custo` | categoria | — | Natureza do custo | SERVICO_CONTRATADO, EQUIPAMENTO, MATERIAL, LICENCAS_E_NUVEM, OUTROS, INDIRETO |
| `id_atividade` | texto | — | Atividade apropriada | Chave da tabela 07; vazio nas frentes AGIL e GESTAO |
| `codigo_eap` | texto | — | Pacote de trabalho apropriado | Chave da tabela 06 |
| `id_contrato` | texto | — | Contrato | Chave da tabela 30; vazio em compras avulsas |
| `id_fornecedor` | texto | — | Fornecedor | Chave da tabela 29 |
| `documento` | texto | — | Documento de origem | MED-contrato-nº (medição da tabela 31), NF-atividade-nº (nota avulsa), SM-nº (mudança aprovada), OC-nº (ocorrência de risco), NF-GES e NF-NUV (notas mensais) |
| `descricao` | texto | — | Histórico do lançamento |  |
| `valor_rs` | decimal | R$ | Valor pago |  |

### 20_sprint_itens — Itens de cada sprint

O que entrou em cada sprint, como entrou e se foi concluído nela.

**Granularidade:** Uma linha por sprint e item

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_sprint` | texto | — | Sprint | Chave da tabela 15 |
| `id_item` | texto | — | Item | Chave da tabela 14 |
| `pontos` | inteiro | pontos de história | Pontos do item |  |
| `origem_na_sprint` | categoria | — | Como o item entrou na sprint | PLANEJAMENTO (escolhido no planejamento), TRANSBORDO (veio inacabado da sprint anterior), ADICIONADO_DURANTE (entrou com a sprint em curso) |
| `concluido_na_sprint` | inteiro | 0 ou 1 | Se o item chegou a CONCLUIDO nesta sprint | A velocidade da sprint é a soma dos pontos com 1 |

### 21_itens_transicoes — Histórico de transições dos itens

Cada mudança de coluna no quadro, como no histórico do Jira.

**Granularidade:** Uma linha por mudança de status

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_transicao` | texto | — | Identificador da transição |  |
| `id_item` | texto | — | Item | Chave da tabela 14 |
| `data` | data | — | Dia da mudança |  |
| `status_origem` | categoria | — | Coluna de onde saiu | A_FAZER, EM_ANDAMENTO, EM_REVISAO, EM_TESTE |
| `status_destino` | categoria | — | Coluna para onde foi | EM_ANDAMENTO, EM_REVISAO, EM_TESTE, CONCLUIDO. EM_TESTE → EM_ANDAMENTO é reprovação no teste |
| `id_pessoa` | texto | — | Quem moveu o item | Chave da tabela 04 |

### 22_impedimentos — Impedimentos

Bloqueios registrados nas reuniões diárias.

**Granularidade:** Uma linha por impedimento

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_impedimento` | texto | — | Identificador |  |
| `id_item` | texto | — | Item bloqueado | Chave da tabela 14 |
| `data_abertura` | data | — | Dia em que o bloqueio começou |  |
| `data_fechamento` | data | — | Dia em que foi resolvido | Vazio = ainda aberto |
| `tipo_impedimento` | categoria | — | Causa do bloqueio | DEPENDENCIA_EXTERNA, DEFINICAO_PENDENTE, AMBIENTE_INDISPONIVEL, AGUARDANDO_OUTRO_TIME |
| `dias_uteis_bloqueado` | inteiro | du | Duração do bloqueio | Vazio enquanto aberto |
| `id_pessoa` | texto | — | Quem registrou | Chave da tabela 04 |

### 23_implantacoes — Implantações de versão

Cada publicação de versão nos ambientes de homologação e de produção.

**Granularidade:** Uma linha por implantação

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_implantacao` | texto | — | Identificador |  |
| `data` | data | — | Dia da implantação |  |
| `id_sprint` | texto | — | Sprint | Chave da tabela 15 |
| `ambiente` | categoria | — | Onde a versão foi publicada | HOMOLOGACAO, PRODUCAO |
| `versao` | texto | — | Número da versão |  |
| `itens_implantados` | inteiro | itens | Quantidade de itens do backlog na versão |  |
| `tempo_ate_producao_h` | decimal | h | Tempo entre o código pronto e a publicação | Mede o tempo de espera para mudanças |
| `falhou` | inteiro | 0 ou 1 | Se a implantação causou falha e precisou de correção ou retorno |  |
| `tempo_restauracao_h` | decimal | h | Tempo para restaurar o serviço | Só quando falhou = 1 |

### 24_defeitos — Defeitos

Defeitos encontrados, com o item que os originou. Cada defeito também é um item BUG no backlog.

**Granularidade:** Uma linha por defeito

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_defeito` | texto | — | Identificador |  |
| `id_item_defeito` | texto | — | Item BUG correspondente no backlog | Chave da tabela 14 |
| `id_item_origem` | texto | — | Item cuja entrega causou o defeito | Chave da tabela 14 |
| `severidade` | categoria | — | Gravidade | BAIXA, MEDIA, ALTA, CRITICA |
| `ambiente_detectado` | categoria | — | Onde o defeito foi encontrado | TESTE, HOMOLOGACAO, PRODUCAO (escapou para o usuário) |
| `data_abertura` | data | — | Dia em que foi registrado |  |
| `data_resolucao` | data | — | Dia em que o item BUG foi concluído | Vazio = em aberto |

### 25_inspecoes_aceite — Inspeções e testes de aceite

Verificações de qualidade das entregas da trilha preditiva.

**Granularidade:** Uma linha por inspeção

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_inspecao` | texto | — | Identificador |  |
| `data` | data | — | Dia da inspeção |  |
| `id_atividade` | texto | — | Atividade inspecionada | Chave da tabela 07 |
| `tipo_inspecao` | categoria | — | Tipo de verificação | LISTA_DE_VERIFICACAO, AUDITORIA_DOCUMENTAL, FAT, SAT, TESTE_A_FRIO, INSPECAO_DE_RECEBIMENTO, HOMOLOGACAO, TESTE_DE_ACEITACAO_DO_USUARIO |
| `itens_verificados` | inteiro | itens | Itens conferidos |  |
| `itens_nao_conformes` | inteiro | itens | Itens reprovados |  |
| `resultado` | categoria | — | Resultado | APROVADO, APROVADO_COM_RESSALVA, REPROVADO |
| `id_fornecedor` | texto | — | Fornecedor responsável pela entrega | Chave da tabela 29; vazio = equipe própria |
| `horas_retrabalho` | decimal | h | Horas gastas para corrigir |  |
| `custo_retrabalho_rs` | decimal | R$ | Custo estimado da correção | Custo da não qualidade; já está dentro dos custos realizados |

### 26_riscos_registro — Registro de riscos

Riscos identificados, com probabilidade, impacto, resposta e situação na data do arquivo.

**Granularidade:** Uma linha por risco

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_risco` | texto | — | Identificador | R01, R02... |
| `data_identificacao` | data | — | Quando o risco entrou no registro |  |
| `tipo_risco` | categoria | — | Ameaça ou oportunidade | AMEACA, OPORTUNIDADE |
| `categoria` | categoria | — | Fonte do risco | TECNICO, FORNECEDOR, REGULATORIO, PESSOAS, MERCADO, EXTERNO, ESCOPO, SEGURANCA |
| `descricao` | texto | — | Evento incerto |  |
| `causa` | texto | — | Causa-raiz |  |
| `probabilidade_pct` | inteiro | % | Probabilidade estimada de ocorrer |  |
| `impacto_custo_rs` | decimal | R$ | Impacto em custo se ocorrer | Negativo nas oportunidades (ganho) |
| `impacto_prazo_du` | inteiro | du | Impacto em prazo se ocorrer | Negativo nas oportunidades |
| `frente` | categoria | — | Onde o risco atua | PREDITIVA, AGIL, PROJETO |
| `id_atividade` | texto | — | Atividade mais exposta | Chave da tabela 07; vazio se não se aplica |
| `estrategia_resposta` | categoria | — | Estratégia planejada | Ameaças: EVITAR, MITIGAR, TRANSFERIR, ACEITAR. Oportunidades: EXPLORAR, MELHORAR |
| `custo_resposta_rs` | decimal | R$ | Custo previsto da resposta | Zero quando a estratégia é aceitar |
| `id_responsavel` | texto | — | Dono do risco | Chave da tabela 04 |
| `status` | categoria | — | Situação na data do arquivo | ABERTO, OCORRIDO, ENCERRADO (atividade exposta terminou sem o risco ocorrer) |

### 27_riscos_ocorrencias — Ocorrências (riscos materializados e imprevistos)

Eventos que aconteceram, com o impacto real. Linha sem id_risco é imprevisto: não estava no registro.

**Granularidade:** Uma linha por ocorrência

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_ocorrencia` | texto | — | Identificador | OC-001... Aparece no campo documento da tabela 19 |
| `data` | data | — | Dia da ocorrência |  |
| `id_risco` | texto | — | Risco que se materializou | Chave da tabela 26; vazio = não identificado |
| `descricao` | texto | — | O que aconteceu |  |
| `frente` | categoria | — | Frente afetada | PREDITIVA, AGIL |
| `id_atividade` | texto | — | Atividade afetada | Chave da tabela 07 |
| `impacto_custo_real_rs` | decimal | R$ | Custo causado |  |
| `impacto_prazo_real_du` | inteiro | du | Atraso causado na atividade |  |
| `custo_ja_incluido_em_pagamentos` | categoria | — | Se o custo já está dentro de outros lançamentos | SIM = efeito de câmbio, já embutido nas medições pagas (não somar de novo); NAO = há um lançamento OC próprio na tabela 19 |

### 28_mudancas_solicitacoes — Solicitações de mudança

Pedidos formais de mudança, com impacto e decisão.

**Granularidade:** Uma linha por solicitação

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_mudanca` | texto | — | Identificador | SM-001... |
| `data_abertura` | data | — | Dia do pedido |  |
| `id_solicitante` | texto | — | Quem pediu | Chave da tabela 03 |
| `descricao` | texto | — | O que se pede |  |
| `tipo_mudanca` | categoria | — | Natureza | ESCOPO, PRAZO, TECNICA |
| `frente` | categoria | — | Frente afetada | PREDITIVA, AGIL |
| `id_atividade` | texto | — | Atividade afetada | Chave da tabela 07; vazio na frente ágil |
| `impacto_custo_rs` | decimal | R$ | Custo estimado da mudança |  |
| `impacto_prazo_du` | inteiro | du | Prazo adicional estimado na atividade |  |
| `impacto_pontos` | inteiro | pontos de história | Pontos adicionados ao backlog | Só na frente ágil |
| `status` | categoria | — | Situação | EM_ANALISE, APROVADA, REJEITADA |
| `data_decisao` | data | — | Dia da decisão | Vazio enquanto em análise |
| `nivel_decisor` | categoria | — | Quem decidiu | GERENTE, PATROCINADOR, COMITE. Compare com a tabela 05 |
| `implementada` | categoria | — | Se a mudança aprovada já foi executada | SIM, NAO; vazio se não aprovada |

### 29_fornecedores — Fornecedores

Cadastro de fornecedores e parceiros.

**Granularidade:** Uma linha por fornecedor

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_fornecedor` | texto | — | Identificador | F01, F02... |
| `nome` | texto | — | Razão social | Nome fictício |
| `localidade` | texto | — | Cidade e estado ou país |  |
| `categoria` | texto | — | O que fornece |  |

### 30_contratos — Contratos

Contratos do projeto, com tipo de remuneração e regra de multa.

**Granularidade:** Uma linha por contrato

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_contrato` | texto | — | Identificador | CT01, CT02... |
| `id_fornecedor` | texto | — | Contratado | Chave da tabela 29 |
| `objeto` | texto | — | O que o contrato cobre |  |
| `tipo_contrato` | categoria | — | Forma de remuneração | PRECO_FIXO, PRECO_UNITARIO (paga a quantidade medida), TEMPO_E_MATERIAL (paga o tempo gasto), CUSTO_REEMBOLSAVEL, ASSINATURA (mensalidade) |
| `moeda` | categoria | — | Moeda do contrato | BRL, USD, EUR. Valores das tabelas sempre em R$, pelo câmbio do orçamento |
| `valor_contratado_rs` | decimal | R$ | Valor do contrato na linha de base |  |
| `multa_atraso_pct_dia` | decimal | % por dia corrido | Multa por dia de atraso da entrega final | Só em PRECO_FIXO; zero nos demais |
| `teto_multa_pct` | decimal | % | Limite da multa sobre o valor do contrato |  |

### 31_contratos_medicoes — Medições e marcos de pagamento

Marcos de pagamento dos contratos de preço fixo e de equipamentos (previstos e realizados) e medições mensais dos demais (só as realizadas).

**Granularidade:** Uma linha por marco ou medição

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_medicao` | texto | — | Identificador | MED-contrato-nº. Aparece no campo documento da tabela 19 |
| `id_contrato` | texto | — | Contrato | Chave da tabela 30 |
| `id_atividade` | texto | — | Atividade medida | Chave da tabela 07 |
| `descricao_marco` | texto | — | O que está sendo pago |  |
| `data_prevista` | data | — | Data prevista na linha de base | Nas medições mensais é igual à data real |
| `valor_previsto_rs` | decimal | R$ | Valor previsto |  |
| `data_real` | data | — | Data em que a medição foi aceita e paga | Vazio = pendente |
| `valor_pago_rs` | decimal | R$ | Valor pago | Pode diferir do previsto por câmbio, quantidade ou tempo |
| `aceite` | categoria | — | Resultado do aceite | APROVADO, APROVADO_COM_RESSALVA, PENDENTE |
| `nao_conformidades` | inteiro | ocorrências | Não conformidades apontadas no aceite |  |

### 32_propostas_fornecedores — Propostas da contratação em aberto

Propostas recebidas para um pacote ainda não contratado. A escolha é do grupo.

**Granularidade:** Uma linha por proposta

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_proposta` | texto | — | Identificador |  |
| `pacote` | texto | — | O que está sendo contratado |  |
| `id_fornecedor` | texto | — | Proponente | Chave da tabela 29. Verifique o histórico do proponente no projeto |
| `preco_rs` | decimal | R$ | Preço proposto |  |
| `prazo_du` | inteiro | du | Prazo de execução proposto |  |
| `nota_tecnica` | decimal | 0 a 10 | Nota da avaliação técnica |  |
| `projetos_similares` | inteiro | projetos | Experiência comprovada |  |
| `garantia_meses` | inteiro | meses | Garantia oferecida |  |
| `condicao_pagamento` | texto | — | Condição de pagamento |  |

### 33_reunioes — Reuniões

Reuniões de acompanhamento e cerimônias ágeis, com presença e resultado.

**Granularidade:** Uma linha por reunião

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_reuniao` | texto | — | Identificador |  |
| `data` | data | — | Dia |  |
| `tipo_reuniao` | categoria | — | Tipo | STATUS_SEMANAL, COMITE_DIRETOR, PLANEJAMENTO_DA_SPRINT, REVISAO_DA_SPRINT, RETROSPECTIVA |
| `duracao_min` | inteiro | min | Duração |  |
| `convidados` | inteiro | pessoas | Pessoas convidadas |  |
| `presentes` | inteiro | pessoas | Pessoas presentes |  |
| `patrocinador_presente` | inteiro | 0 ou 1 | Se o patrocinador participou |  |
| `decisoes_tomadas` | inteiro | decisões | Decisões registradas em ata |  |
| `pendencias_abertas` | inteiro | pendências | Assuntos que saíram sem decisão |  |
| `ata_publicada` | inteiro | 0 ou 1 | Se a ata foi distribuída |  |

### 34_engajamento_mensal — Engajamento mensal das partes interessadas

Avaliação mensal do gerente do projeto sobre cada parte interessada.

**Granularidade:** Uma linha por mês e parte interessada

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `mes` | data | — | Primeiro dia do mês avaliado |  |
| `id_parte` | texto | — | Parte interessada | Chave da tabela 03 |
| `nivel_engajamento` | categoria | — | Nível observado no mês | DESCONHECE, RESISTENTE, NEUTRO, APOIA, LIDERA |
| `satisfacao` | decimal | 0 a 10 | Satisfação declarada com o projeto |  |
| `interacoes_no_mes` | inteiro | contatos | Reuniões e contatos registrados com a parte |  |

### 35_pulso_equipe — Pulso da equipe ágil

Pesquisa rápida respondida na retrospectiva de cada sprint.

**Granularidade:** Uma linha por sprint

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_sprint` | texto | — | Sprint | Chave da tabela 15 |
| `satisfacao_media` | decimal | 1 a 5 | Média da satisfação do time |  |
| `respostas` | inteiro | pessoas | Quantidade de respostas |  |

### 36_okr_medicoes — Objetivos e resultados-chave

Medições mensais dos resultados-chave do projeto.

**Granularidade:** Uma linha por resultado-chave e mês

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_objetivo` | texto | — | Objetivo | O1, O2 |
| `objetivo` | texto | — | Texto do objetivo |  |
| `id_resultado_chave` | texto | — | Resultado-chave | KR1 a KR6 |
| `resultado_chave` | texto | — | Texto do resultado-chave |  |
| `unidade` | texto | — | Unidade de medida |  |
| `valor_base` | decimal | ver unidade | Valor no início |  |
| `meta` | decimal | ver unidade | Valor a atingir |  |
| `sentido` | categoria | — | Direção desejada | MAIOR_MELHOR, MENOR_MELHOR |
| `data_medicao` | data | — | Data da medição | Último dia do mês (ou a data de status) |
| `valor` | decimal | ver unidade | Valor medido |  |

### 37_funil_piloto_semanal — Funil semanal do piloto

Uso do produto digital pelos usuários do piloto, desde a Release 1.

**Granularidade:** Uma linha por semana

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `semana_inicio` | data | — | Segunda-feira da semana |  |
| `alcance` | inteiro | pessoas | Pessoas alcançadas ou habilitadas na semana | Topo do funil (conhecimento) |
| `cadastros` | inteiro | pessoas | Novos cadastros na semana | Aquisição |
| `ativados` | inteiro | pessoas | Novos cadastrados que fizeram a primeira ação de valor | Ativação |
| `ativos_na_semana` | inteiro | pessoas | Usuários que usaram o produto na semana |  |
| `retidos_4_semanas` | inteiro | pessoas | Ativos de quatro semanas atrás que continuam ativos | Retenção |
| `receita_rs` | decimal | R$ | Receita gerada na semana | Zero quando o produto é de uso interno |
| `indicacoes` | inteiro | pessoas | Indicações feitas por usuários | Recomendação |
| `nps` | inteiro | −100 a 100 | NPS da semana |  |
| `chamados_suporte` | inteiro | chamados | Chamados abertos pelos usuários |  |

## Bloco E. Modelo 3D

### 38_elementos_3d — Elementos do modelo 3D

Elementos da cena 3D, cada um com posição e volume e ligado a atividades, a um épico ou a releases. Nas expansões de linha são as partes do que será construído; o grupo troca os blocos por formas reconhecíveis e monta o modelo em etapas.

**Granularidade:** Uma linha por elemento

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_elemento` | texto | — | Identificador | EL01, EL02... |
| `nome_elemento` | texto | — | Nome a exibir |  |
| `tipo_elemento` | categoria | — | Tipo | AREA, EDIFICACAO, EQUIPAMENTO, EQUIPAMENTO_EXISTENTE, UTILIDADE, HARDWARE, MODULO_DIGITAL, UNIDADE_DE_IMPLANTACAO |
| `x` | decimal | m | Coordenada x do canto de origem | Nos produtos digitais a cena é esquemática: 1 unidade = 1 m |
| `y` | decimal | m | Coordenada y do canto de origem |  |
| `z` | decimal | m | Cota da base |  |
| `largura` | decimal | m | Dimensão em x |  |
| `comprimento` | decimal | m | Dimensão em y |  |
| `altura` | decimal | m | Dimensão em z |  |
| `vinculo_tipo` | categoria | — | A que o elemento está ligado | ATIVIDADE, EPICO, RELEASE, NENHUM |
| `vinculo_ids` | texto | — | Identificadores ligados, separados por ponto e vírgula | Chaves das tabelas 07, 13 ou 16 |
| `ordem_de_implantacao` | inteiro | posição | Ordem em que a unidade recebe a implantação | Só em UNIDADE_DE_IMPLANTACAO: a unidade n de N está pronta quando o avanço do vínculo ≥ n ÷ N |

## Bloco F. Pessoas, custos de pessoal e produtividade

### 39_cargos_salarios — Folha da equipe do projeto

Remuneração mensal, encargos, benefícios e reajuste previsto de cada pessoa da equipe. É a origem do custo por hora da tabela 04.

**Granularidade:** Uma linha por pessoa

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_pessoa` | texto | — | Identificador da pessoa | Chave da tabela 04 |
| `vinculo` | categoria | — | Forma de contratação | CLT, PJ |
| `remuneracao_mensal_rs` | decimal | R$/mês | Salário-base (CLT) ou valor mensal do contrato (PJ) | Sem encargos e sem benefícios |
| `encargos_pct` | decimal | % | Encargos sociais e provisões sobre o salário-base | CLT: férias, 13º, FGTS e contribuições. PJ: 0 |
| `beneficios_mensais_rs` | decimal | R$/mês | Benefícios pagos pela empresa | Plano de saúde, alimentação e transporte. PJ: 0 |
| `horas_mensais` | inteiro | h/mês | Horas produtivas consideradas por mês | Custo por hora = custo mensal ÷ horas_mensais, arredondado para o inteiro |
| `reajuste_previsto_pct` | decimal | % | Reajuste previsto da remuneração | Aplica-se sobre remuneracao_mensal_rs a partir de mes_do_reajuste |
| `mes_do_reajuste` | data | — | Primeiro mês com a remuneração reajustada | Primeiro dia do mês |

### 40_alocacao_planejada — Alocação planejada da equipe

Horas que a linha de base previa para cada pessoa, mês a mês, e a capacidade dela no mês. Quem entrou depois como substituto não aparece.

**Granularidade:** Uma linha por pessoa e mês

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_pessoa` | texto | — | Identificador da pessoa | Chave da tabela 04 |
| `mes` | data | — | Mês de referência | Primeiro dia do mês |
| `horas_planejadas` | decimal | h | Horas previstas para a pessoa no mês | Preditiva: horas orçadas das atividades da disciplina, distribuídas pela duração da linha de base |
| `capacidade_horas` | decimal | h | Horas disponíveis da pessoa no mês | Dias úteis do mês × horas_por_dia × alocacao_pct |

### 41_produtividade_referencia — Referência de produtividade das equipes

Atividades com serviço mensurável, executadas por equipes de fornecedores: quantidade total, produtividade e equipe previstas no plano.

**Granularidade:** Uma linha por atividade mensurável

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_atividade` | texto | — | Atividade da tabela 07 |  |
| `servico` | texto | — | Serviço medido |  |
| `unidade` | texto | — | Unidade de medida do serviço | m, m2, m3, t, ponto, un, tela, peca, servico, local, cenario |
| `quantidade_total` | decimal | unidade do serviço | Quantidade total prevista para a atividade |  |
| `produtividade_planejada` | decimal | unidade por Hh | Quantidade de serviço por homem-hora prevista no plano | Hh = horas trabalhadas somadas de toda a equipe |
| `equipe_planejada_pessoas` | inteiro | pessoas | Tamanho da equipe previsto | Duração estimada = quantidade ÷ (produtividade × equipe × horas_por_dia) |
| `id_contrato` | texto | — | Contrato do fornecedor que executa | Chave da tabela 30 |

### 42_producao_semanal — Produção semanal das equipes

Quantidade executada, homens-hora e efetivo de cada atividade mensurável, semana a semana.

**Granularidade:** Uma linha por atividade e semana

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `semana_fim` | data | — | Sexta-feira que encerra a semana |  |
| `id_atividade` | texto | — | Atividade da tabela 41 |  |
| `quantidade_executada` | decimal | unidade do serviço | Quantidade medida na semana | Não acumulada |
| `hh_trabalhadas` | inteiro | Hh | Homens-hora gastos na semana | Produtividade real = quantidade ÷ Hh |
| `efetivo_medio` | decimal | pessoas | Número médio de pessoas da equipe na semana | Compare com equipe_planejada_pessoas |

## Bloco G. Cenários de decisão

### 43_cenarios — Cenários levados ao comitê

Opções de decisão em aberto na data de status: seguir, recuperar prazo, cortar, ampliar ou trocar escopo e mudar a forma de implantação.

**Granularidade:** Uma linha por cenário

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_cenario` | texto | — | Identificador do cenário | C1 a C6. C1 é a referência |
| `nome_cenario` | texto | — | Nome curto |  |
| `tipo_cenario` | categoria | — | Natureza da decisão | SEGUIR, RECUPERAR_PRAZO, CORTE_DE_ESCOPO, AUMENTO_DE_ESCOPO, MUDANCA_DE_ESCOPO, CAMINHO_ALTERNATIVO |
| `descricao` | texto | — | O que o cenário propõe |  |
| `id_proponente` | texto | — | Parte interessada que defende o cenário | Chave da tabela 03 |
| `variacao_beneficio_pct` | decimal | % | Mudança no benefício bruto anual do caso de negócio | Aplica-se a todos os anos da tabela 02 |
| `variacao_custo_operacional_anual_rs` | decimal | R$/ano | Mudança no custo operacional anual | Soma-se ao custo operacional dos anos 1 em diante |
| `investimento_adicional_rs` | decimal | R$ | Desembolso extra que não está nas tabelas 44 a 46 |  |
| `parcela_beneficio_antecipada_pct` | decimal | % | Parcela do benefício que começa mais cedo | Começa no término de id_atividade_gatilho; o restante começa no término do projeto |
| `id_atividade_gatilho` | texto | — | Atividade cujo término libera a parcela antecipada | Vazio quando não há antecipação |
| `combinavel_com` | texto | — | Cenários que podem ser adotados junto com este | Lista separada por ponto e vírgula |

### 44_cenario_atividades — Mudanças na rede por cenário

O que cada cenário inclui, exclui ou altera nas atividades da trilha preditiva.

**Granularidade:** Uma linha por cenário e atividade afetada

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_cenario` | texto | — | Cenário | Chave da tabela 43 |
| `acao` | categoria | — | O que muda | INCLUIR, EXCLUIR, ALTERAR_DURACAO |
| `id_atividade` | texto | — | Atividade afetada | Atividades novas usam N01, N02... |
| `nome_atividade` | texto | — | Nome da atividade |  |
| `disciplina` | categoria | — | Disciplina | Códigos da tabela 07 |
| `duracao_du` | inteiro | dias úteis | Duração no cenário | INCLUIR: duração da atividade nova. ALTERAR_DURACAO: nova duração total. EXCLUIR: 0 |
| `predecessoras` | texto | — | Predecessoras da atividade nova | Formato id:tipo:defasagem, separadas por ponto e vírgula. Vazio = pode começar no dia útil seguinte ao status |
| `sucessoras` | texto | — | Atividades que passam a depender da atividade nova | Mesmo formato |
| `custo_adicional_rs` | decimal | R$ | Custo a mais (positivo) ou economia (negativo) da mudança |  |

### 45_cenario_backlog — Mudanças no backlog por cenário

Itens que cada cenário inclui ou exclui do backlog do produto.

**Granularidade:** Uma linha por cenário e item

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_cenario` | texto | — | Cenário | Chave da tabela 43 |
| `acao` | categoria | — | O que muda | INCLUIR, EXCLUIR |
| `id_item` | texto | — | Item afetado | Itens novos terminam em -N1, -N2... |
| `titulo` | texto | — | Título do item |  |
| `id_epico` | texto | — | Épico do item | Chave da tabela 13 |
| `id_release` | texto | — | Release do item | R1, R2, R3 |
| `pontos` | inteiro | pontos | Pontos de história |  |

### 46_cenario_recursos — Reforço de equipe por cenário

Contratações temporárias previstas em cada cenário e o ganho de velocidade esperado.

**Granularidade:** Uma linha por cenário e papel

| Campo | Tipo | Unidade | Descrição | Domínio e observações |
|---|---|---|---|---|
| `id_cenario` | texto | — | Cenário | Chave da tabela 43 |
| `papel` | texto | — | Função contratada |  |
| `senioridade` | categoria | — | Nível de experiência | JR, PL, SR |
| `quantidade` | inteiro | pessoas | Número de pessoas |  |
| `custo_mensal_rs` | decimal | R$/mês | Custo mensal por pessoa, com encargos |  |
| `meses` | inteiro | meses | Duração da contratação |  |
| `ganho_velocidade_pontos_por_sprint` | decimal | pontos por sprint | Aumento esperado na velocidade do time | Por pessoa, depois da rampa |
| `sprints_de_rampa` | inteiro | sprints | Sprints sem ganho depois da entrada |  |

## Convenções oficiais de cálculo

1. **Duração da linha de base.** Atividade ESTIMADA: duração = (O + 4M + P) ÷ 6, arredondada para cima; desvio-padrão = (P − O) ÷ 6. Atividade MARCO_AGIL: usa `duracao_fixa_du`.
2. **Rede.** TI: início ≥ término da predecessora + 1 + defasagem. II: início ≥ início da predecessora + defasagem. Tudo em dias úteis; o dia útil 1 é `data_inicio_projeto`. A linha de base usa as datas mais cedo.
3. **Orçamento no término (ONT).** Frente preditiva: soma da tabela 09. Frente ágil: soma de `orcamento_sprint_rs` das sprints com `planejada_na_linha_de_base` = 1. Projeto: soma das duas. A gestão do projeto (categoria INDIRETO e horas GESTAO) é acompanhada à parte.
4. **Valor planejado (VP).** Preditiva: custo orçado da atividade distribuído linearmente pelos dias úteis da sua duração na linha de base. Ágil: orçamento das sprints planejadas encerradas até a data (sprint em curso: proporcional aos dias úteis decorridos).
5. **Valor agregado (VA).** Preditiva: último `avanco_acumulado_pct` informado até a data × custo orçado da atividade. Ágil: ONT da frente ágil × (pontos concluídos ÷ pontos totais) do escopo da linha de base, que são os itens com `origem` = PLANO_INICIAL e prioridade diferente de WONT.
6. **Custo real (CR).** Lançamentos da tabela 19 da frente, até a data, mais as horas da tabela 18 (semanas encerradas até a data) × `custo_hora_rs`, com as horas extras multiplicadas por `fator_hora_extra`. ATIVIDADE vai para a preditiva, SPRINT para a ágil.
7. **Índices.** IDP = VA ÷ VP; IDC = VA ÷ CR; estimativa no término (ENT) = ONT ÷ IDC; índice de desempenho para terminar (IDPT) = (ONT − VA) ÷ (ONT − CR).
8. **Velocidade.** Soma dos pontos dos itens com `concluido_na_sprint` = 1, de todos os tipos e origens. Velocidade média = média das últimas cinco sprints encerradas.
9. **Tempo de ciclo.** Dias úteis da primeira entrada em EM_ANDAMENTO até a conclusão, contando os dois extremos. **Tempo de espera (lead time).** Dias úteis da criação até a conclusão.
10. **Previsão de release.** Pontos restantes da release j = pontos dos itens não concluídos, com prioridade diferente de WONT, das releases 1 a j. Sprints restantes = pontos restantes ÷ velocidade média, arredondado para cima. Data prevista = fim da sprint correspondente.
11. **Previsão de término pela rede.** Atividade concluída: datas reais. Em andamento: termina em (data de status + duração da linha de base × (1 − avanço), arredondada para cima). Não iniciada: duração da linha de base, começando depois das predecessoras e nunca antes do dia útil seguinte ao status. Marco ágil não concluído: termina na data prevista da release.
12. **Valor monetário esperado (VME).** Probabilidade × impacto em custo. A exposição do projeto é a soma do VME das ameaças abertas.
13. **Implantação (métricas DORA).** Frequência = implantações em produção por semana; tempo de espera = mediana de `tempo_ate_producao_h`; taxa de falha = implantações com falha ÷ total; tempo de restauração = média de `tempo_restauracao_h`.
14. **Multa contratual.** Dias corridos de atraso do último marco do contrato × `multa_atraso_pct_dia` × valor do contrato, limitada a `teto_multa_pct`.
15. **Seleção de fornecedor.** Nota = Σ peso × nota normalizada. Preço e prazo: menor valor ÷ valor da proposta. Técnica: nota ÷ 10. Experiência e garantia: valor ÷ maior valor.
16. **Caso de negócio.** Fluxo líquido do ano = benefício bruto − custo operacional − investimento. VPL com a taxa mínima de atratividade; payback simples com interpolação dentro do ano.
17. **Custo de pessoal.** Custo mensal da pessoa = remuneração × (1 + encargos) + benefícios (tabela 39). Custo por hora = custo mensal ÷ `horas_mensais`, arredondado para o inteiro: é o `custo_hora_rs` da tabela 04. O custo de pessoal do projeto vem das horas apontadas (convenção 6), não da folha.
18. **Utilização e alocação.** Capacidade = dias úteis no projeto × `horas_por_dia` × `alocacao_pct`. Utilização = horas apontadas ÷ capacidade. A semana pertence ao mês da sua `semana_inicio`. Desvio de alocação = horas apontadas − horas planejadas (tabela 40), nos meses fechados. Na frente preditiva as pessoas são compartilhadas com outras áreas da empresa: compare as horas apontadas com as planejadas, não com a capacidade.
19. **Reajuste.** Impacto = média mensal de horas apontadas pela pessoa nos três últimos meses fechados × meses entre o reajuste (ou o mês seguinte ao status, o que vier depois) e o término previsto do projeto × `custo_hora_rs` × reajuste.
20. **Produtividade.** Real = quantidade executada ÷ Hh (tabela 42). Índice de produtividade = real ÷ planejada. Índice de efetivo = efetivo médio ÷ equipe planejada. Duração restante = quantidade restante ÷ (produtividade real acumulada × efetivo médio das três últimas semanas × `horas_por_dia`), arredondada para cima. Time ágil: pontos concluídos pelo responsável ÷ horas apontadas em sprints; custo por ponto = custo dessas horas ÷ pontos.
21. **Prazo de um cenário.** Parte-se da previsão pela rede (convenção 11). INCLUIR cria a atividade com as ligações indicadas; EXCLUIR zera a duração e mantém as ligações; ALTERAR_DURACAO troca a duração total (em andamento: reduz a duração restante na mesma quantidade de dias, com mínimo de 1). No backlog, item excluído sai dos pontos restantes e item incluído entra na release indicada. Com reforço, a velocidade das sprints depois da rampa é a média mais o ganho.
22. **Custo de um cenário.** Estimativa no término do cenário = ENT atual + custos adicionais da tabela 44 + (pontos incluídos − pontos excluídos) × custo real por ponto + custo dos recursos da tabela 46 (quantidade × custo mensal × meses) + investimento adicional da tabela 43. Custo real por ponto = custo real da frente ágil ÷ pontos concluídos. Custo do atraso = dias úteis além da data contratual × `custo_do_atraso_por_du_rs`.
23. **Valor de um cenário.** Refazer o fluxo da tabela 02: benefício × (1 + variação), custo operacional + variação anual, ano 0 acrescido de (ENT do cenário − ONT). O atraso reduz o primeiro ano: fluxo líquido do ano 1 × meses de atraso ÷ 12, com meses = dias corridos entre o término da linha de base e o término previsto ÷ 30,4. Com parcela antecipada, o atraso efetivo é a média ponderada entre o atraso do gatilho e o atraso do término. Resultado do cenário = VPL − custo do atraso.
