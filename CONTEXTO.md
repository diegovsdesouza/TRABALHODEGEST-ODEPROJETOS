# CONTEXTO — ENGN62 · Trabalho Final "Sala de Guerra das Duas Trilhas" (UFBA 2026.2)

> **Como usar:** toda conversa nova com a IA começa por este arquivo (regra 1 do enunciado). Peça **uma tarefa pequena por conversa e por branch** e anexe os arquivos que ela pedir.

## 1. O caso

- **Grupo 7 · Plásticos Abrantes (Camaçari/BA):** linha de injeção e pintura de para-choques, fornecida a uma montadora.
- **Contexto:** expansão de linha de produção, então o grupo entrega o **modelo 3D** (R12/D17), não mockups.
- **Projeto híbrido:**
  - **Trilha preditiva:** 59 atividades. Cobre engenharia, compra e importação de 3 equipamentos (injetora de 3.200 t, cabine de pintura robotizada, transportador aéreo e robôs), obra civil e utilidades, elétrica e automação, montagem, NR-12, comissionamento e treinamento. Ferramenta: **ProjectLibre**.
  - **Trilha ágil:** 94 itens no backlog, 5 épicos, sprints de 2 semanas desde 04/05/2026 e releases planejadas nas sprints S05, S11 e S17. Ferramenta: **Jira**.
  - **Ponto de contato entre as trilhas:** o SAT (A47) depende da Release 2 (A58), e o aceite final (A56) depende da Release 3 (A59).
- **Números-chave:**
  - Orçamento no término (ONT): R$ 39.009.276, sendo R$ 38.271.476 da preditiva e R$ 737.800 da ágil.
  - Reservas: contingência de R$ 831.000 e gerencial de R$ 1.170.000.
  - Custo do atraso: R$ 50.100 por dia útil. TMA: 14% a.a.
  - Início em 02/02/2026 (dia útil 1). Término contratual em 07/05/2027 (du 312).
- **Datas dos dados:**
  - Histórico nos CSV até 30/10/2026.
  - Quinzena de campo de 03 a 13/11/2026: vem nos boletins B1 a B10 do dossiê e é **digitada nas telas**.
  - **Data de status: 13/11/2026.**
- **O comitê quer saber:**
  1. quando termina e o que define a data;
  2. quanto custa e de onde vem o desvio;
  3. que escopo entra sem controle;
  4. que fornecedores e decisões seguram o projeto;
  5. se a reserva cobre os riscos;
  6. o que decidir agora, entre os 6 cenários de C1 a C6.

## 2. Regras inegociáveis

1. **Não invente dados.** Use apenas o dossiê, as 46 tabelas, o `dados/DICIONARIO.md` e os boletins. Se faltar algo, pare e diga qual tabela ou campo falta.
2. **Todo número tem fonte e unidade.** Indique a tabela, o filtro e a fórmula (por exemplo: `19_custos_realizados, frente = PREDITIVA, data ≤ 13/11, soma de valor_rs`).
3. **Use as 23 convenções oficiais**, que estão no fim do `DICIONARIO.md`. Se uma regra for ambígua, declare a premissa.
4. **Cálculo sem interpretação vale metade, e achado sem número não conta.** Cada achado tem evidência, causa, impacto (em R$ ou du), ação e dono.
5. **Caderno manuscrito (M1 a M8):** a IA não redige a folha. Ela dá o método e um **gabarito de conferência** separado. Quem assina a folha responde por ela.
6. **Coerência entre ferramentas:** o caminho crítico, o valor agregado e o burndown precisam bater entre o papel, o sistema, o ProjectLibre e o Jira.
7. **Use os dados tratados** em `dados/tratados/`. O que foi corrigido e por quê está em `docs/qualidade-dos-dados.md`.
8. **Segredos:** chaves e senhas nunca vão para o repositório. A chave anon do Supabase é pública; a `service_role` nunca entra aqui.
9. **Atividades e tarefas começam com verbo no infinitivo.** Os pacotes da EAP são entregas (substantivos).

## 3. Entregas e notas (enunciado)

| Parte | O que entra | Nota |
|---|---|---|
| 1 · Escritório de projetos | D1 a D17, .pod + PDF do Gantt, Jira (professor convidado) | 2,0 |
| 1 · Caderno | M1 a M8, à mão, assinadas | 1,0 |
| 2 · Sistema | Funções e dados (R1 a R11, R13 a R16) | 1,5 |
| 2 · Sistema | Modelo 3D (R12) | 0,5 |
| 2 · Sistema | GitHub e publicação (Vercel ou Netlify) | 0,5 |
| 3 · Comitê | Diagnóstico e pelo menos 6 achados | 1,2 |
| 3 · Comitê | Decisão (6 cenários + uma combinação) e relatório de até 15 slides | 0,8 |
| 3 · Comitê | Apresentação e boletim surpresa ao vivo | 2,5 |

**Documentos:**
- D1 Termo de abertura e caso de negócio
- D2 Partes interessadas e comunicação
- D3 EAP e dicionário da EAP
- D4 Cronograma no ProjectLibre
- D5 Orçamento, curva S e reservas
- D6 RACI e histograma
- D7 Backlog e releases no Jira
- D8 Rotina ágil e métricas
- D9 Riscos e reservas
- D10 Aquisições e qualidade
- D11 Mudanças e Bússola de Abordagem
- D12 Estratégia do projeto
- D13 Pessoal e custos de pessoal
- D14 Produtividade das equipes
- D15 Análise financeira
- D16 Cenários e decisão
- D17 Modelo 3D

**Requisitos do sistema:**
- R1 e R2: importar e guardar os dados
- R3: lançar pelas telas (os boletins são digitados por pelo menos 3 pessoas)
- R4: rede e caminho crítico
- R5: valor agregado
- R6: painel ágil
- R7 e R8: riscos e mudanças
- R9 e R10: contratos e partes interessadas
- R11: dashboard
- R12: modelo 3D com controle de data
- R13: assistente de IA
- R14: pessoas e custos
- R15: produtividade
- R16: simulador de cenários

**Também entram:**
- `docs/diario-de-prompts.md`, com 10 entradas de 3 pessoas;
- `docs/qualidade-dos-dados.md`;
- a ficha do grupo, de uma página;
- o formulário de entrega.

## 4. Calendário

| Data | Marco |
|---|---|
| **seg 23/11** | Ponto de controle: 10 min, **com o sistema no ar** |
| **ter 24/11, 23h59** | Entrega digital de tudo |
| qua 25/11 ou seg 30/11 | Apresentação de 25 min: 12 de apresentação, 4 de boletim surpresa ao vivo e 9 de arguição individual |

## 5. Divisão do grupo

| Quem | Documentos | Folhas | Ferramenta | Boletins que lança no sistema | Na apresentação |
|---|---|---|---|---|---|
| Diego (coordenação) | D1, D11, D12, D15, D16, relatório | M7 | GitHub | Confere os números de controle | Abertura, decisão e recomendação |
| Kaique | D3, D4 | M1, M2 | ProjectLibre | B1 (avanço) | Prazo e caminho crítico |
| Marjorie | D5 | M3 | — | B2 e B3 (horas e custos) | Custo e valor agregado |
| José | D9, D10 | M4, M6 | — | B4 e B8 (inspeções, riscos e mudanças) | Riscos, reserva e fornecedores |
| **Guilherme** | D7, D8 | M5 | **Jira (responsável)**: criar o site e o projeto Scrum, convidar o professor, importar o backlog, executar a sprint S14 e capturar o burndown e a velocidade | B5, B6 e B7 (sprint, quadro e impedimentos) | Trilha ágil e escopo fora do controle |
| Arley | D2, D6, D13, D14 | M8 | — | B9 e B10 (reuniões, engajamento e produção) | Pessoas e produtividade |

**Regras para todos:**
- Pelo menos 1 commit e 2 entradas no diário de prompts por pessoa.
- Cada um assina a sua folha e confere a conta contra o gabarito.
- Cada um sabe explicar os números da sua parte na arguição individual.

## 6. O que já está pronto (status)

- **Tratamento de dados:** `scripts/tratamento_dados.py`, com 6 tipos de problema e 48 alterações. Os **13 números de controle do histórico conferem**.
- **Linha de base:** `scripts/cpm.py`. Término em du 304 = **27/04/2027**. O caminho crítico é a cadeia da injetora: A01, A07, A08, A09, A11, A12, A13, A38, A41, A43, A44, A46, A47, A49 e A56.
- **Previsão em 13/11:** `scripts/previsao.py`. Término em **10/05/2027**, 1 du além do contrato, igual ao C1 do dossiê ✅. A data é definida por **A12** (transporte da injetora, 70%). A velocidade média é de 16,0 pontos por sprint; a Release 2 sai em 11/12/2026 e a Release 3 em 05/02/2027.
- **Gabaritos M1 e M2** em `docs/rede-e-caminho-critico.md`.

## 7. Comandos

```bash
python scripts/tratamento_dados.py dados/brutos dados/tratados docs/log_tratamento.csv
python scripts/cpm.py dados/tratados docs/linha_de_base.csv
python scripts/previsao.py dados/tratados docs/linha_de_base.csv
```
