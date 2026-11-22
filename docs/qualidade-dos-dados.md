# Qualidade dos dados — G7 Plásticos Abrantes

**Disciplina:** ENGN62 Gestão de Projetos (UFBA, 2026.2) · **Versão:** 1 · **Data:** 22/11/2026 · **Responsável:** [nome]
**Fonte:** `G7 - Base de dados - Plásticos Abrantes.xlsx` / pasta `dados/` (46 tabelas, histórico até 30/10/2026)
**Script:** `scripts/tratamento_dados.py` · **Log linha a linha:** `docs/log_tratamento.csv`

## 1. Resumo

- Verificamos as 46 tabelas (3.538 linhas). Os testes cobriram:
  - duplicatas exatas e por chave;
  - integridade entre tabelas (chaves órfãs);
  - domínios do dicionário;
  - valores negativos e outliers;
  - coerência entre colunas;
  - reconciliação cruzada (tabela 19 × 31, 14 × 20 × 21, 04 × 39, 41 × 42).
- O planejamento está íntegro:
  - a soma da tabela 09 bate com o ONT da frente preditiva (R$ 38.271.476);
  - PESSOAL_INTERNO = horas orçadas × custo/hora em 100% das linhas;
  - O ≤ M ≤ P em todas as atividades estimadas;
  - não há dependência órfã;
  - o custo/hora da tabela 04 bate com a convenção 17.
- Os problemas estão no Bloco D (execução). São **6 tipos** e **48 alterações**. Nenhuma linha foi apagada sem registro.
- **Depois do tratamento, os 13 números de controle do dossiê (histórico até 30/10) conferem.**

| Cód. | Tabela | Problema | Linhas | Tratamento | Como foi confirmado |
|---|---|---|---|---|---|
| Q1 | 18_apontamento_horas | Linhas duplicadas por inteiro | 9 | Removidas | Ficam 508 linhas, igual ao controle |
| Q2 | 18_apontamento_horas | Casa decimal deslocada (10×): P02 na semana de 16/03 (400 h), P17 na de 05/10 (200 h), P08 em A29 na de 17/08 (170 h) | 3 | Divididas por 10 (40, 20 e 17 h) | Uma semana tem no máximo 40 h normais. Depois da correção, o total dá exatamente 11.708,5 h (controle). Sem a correção, seriam 12.401,5 h |
| Q3 | 19_custos_realizados | Lançamentos da frente preditiva com `codigo_eap` = DIVERSOS e sem atividade | 6 (R$ 779.972,48) | Reapropriados por evidência: a medição na tabela 31 (4) e o código da atividade no número da NF (2) | Nenhum DIVERSOS restante. O total da frente preditiva não muda (R$ 34.632.983,98) |
| Q4 | 17_avanco_semanal | Semanas sem informe no meio da execução (A01, A03, A05, A10, A16 ×2, A22, A50) | 8 | Linha criada repetindo o último avanço informado | Ficam 259 informes (controle). O VA não muda, porque a convenção 5 já usa o último informe |
| Q5 | 21_itens_transicoes | `status_destino` com várias grafias ("Em andamento", "em_teste", "DONE"…) | 14 | Padronizados (maiúsculas, `_`, DONE → CONCLUIDO) | Todos os status caem no domínio. As conclusões batem com a `data_conclusao` da tabela 14 em 65 de 65 itens |
| Q6 | 25_inspecoes_aceite | `resultado` com grafia fora do padrão ("Aprovado", "reprovado") | 8 | Padronizados em maiúsculas | Todos os resultados caem no domínio |

## 2. Itens que parecem erro, mas foram mantidos (premissas)

| Tabela | O que parece erro | Por que foi mantido |
|---|---|---|
| 26 | Impactos negativos em R07 e R11 | São **oportunidades** (`tipo_risco` = OPORTUNIDADE): impacto negativo é ganho |
| 31 | Valor pago acima do previsto no CT03 (injetora, em EUR): +R$ 812.232 | Variação cambial: é a ocorrência do risco R15 (tabela 27). É achado de custo, não erro |
| 31 | CT07 (obra civil, preço unitário) pago 5% a 9% acima em todas as medições: +R$ 291.061 | Quantidade medida acima da orçada. É achado de custo, não erro |
| 40 | P06 com 207,9 h planejadas em mar/26, para uma capacidade de 176 h | Superalocação no plano. Mantido e apontado na análise de pessoas (M8) |
| 42 | Produtividade de A28 de 3,0 un/Hh na última semana (média de 0,56) | Fechamento da atividade com pouca hora. A soma executada bate exatamente com a quantidade total (1.249) |
| 14 | PA-183 e PA-187 com o mesmo título | São dois defeitos diferentes (datas, sprints e responsáveis distintos) |
| 09 | A57, A58 e A59 sem orçamento | São os marcos ágeis; o custo da frente ágil está nas sprints (tabela 15) |
| 38 | `ordem_de_implantacao` toda vazia | O preenchimento é tarefa do grupo (modelo 3D em etapas) |

## 3. Primeiros achados para o comitê

- **Escopo fora do controle:** 7 itens de origem PEDIDO_DIRETO, todos pedidos pelo PI13 (montadora), somam 20 pontos e foram concluídos sem solicitação de mudança. Exemplos: PA-189 "tela de consulta para a linha vizinha" e PA-173 "painel com destaque do mês".
- **Desvio de custo:** concentrado no câmbio da injetora (CT03) e na sobre-medição da obra civil (CT07).

## 4. Impacto, se não tivesse tratado

- As horas ficariam pelo menos 693 h acima do real, só pelo erro de digitação (mais as duplicatas). O CR por pessoa e o custo de pessoal da M8 ficariam inflados.
- R$ 780 mil de custo ficariam fora das atividades. O CR por entrega da EAP (1.1, 1.2, 1.3, 1.4 e 1.7) não fecharia e o IDC dessas entregas sairia otimista.
- O cálculo do tempo de ciclo e o burndown (M5) perderiam transições com status "fora do padrão".
