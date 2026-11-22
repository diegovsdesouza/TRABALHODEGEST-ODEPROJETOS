# Jira · importar o backlog do G7 (responsável: Guilherme)

Arquivo: `backlog_jira.csv` (94 itens do backlog em 30/10 + 5 épicos). A sprint S14 **não** vem no arquivo: ela é executada no quadro, como manda o enunciado (boletins B5 e B6).

1. Crie uma conta gratuita em **atlassian.com/software/jira** e um projeto no modelo **Scrum** (nome: `G7 Plásticos Abrantes`).
2. Crie as versões em **Releases**: **R1** (lançada em 07/08/2026), **R2** (planejada para 02/10/2026) e **R3** (planejada para 25/12/2026).
3. Importe o CSV:
   - pelo menu **⋯ do Backlog → Import issues → CSV**;
   - ou, em projeto company-managed, **⚙ Configurações → Sistema → External System Import → CSV**.
4. No mapeamento de campos, associe as colunas assim:

   | Coluna do CSV | Campo do Jira |
   |---|---|
   | Issue Id | Issue Id |
   | Issue Type | Issue Type |
   | Summary | Summary |
   | Description | Description |
   | Story Points | Story point estimate (ou Story Points) |
   | Priority | Priority |
   | Labels (as duas colunas) | Labels |
   | Fix Version | Fix Version |
   | Parent | Parent |
   | Status | Status |

   Nos valores, deixe **Status** com To Do, In Progress e Done.
5. Confira: 5 épicos, 94 itens, 65 em Done (209 pontos).
6. **Sprint S14 (02 a 13/11):**
   - crie os itens novos PA-195 e PA-196 (boletim B5);
   - coloque na sprint os 13 itens do B5;
   - inicie a sprint e mova os cartões na ordem do B6 (o mesmo do roteiro);
   - feche a sprint.
7. Planeje as sprints futuras com a velocidade real, **16 pontos por sprint**: a R2 cabe em 2 sprints e a R3 em mais 4.
8. Convide o professor e salve em `docs/jira/` as capturas do **burndown** e do **relatório de velocidade**.
