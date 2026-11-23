# D8 · Rotina ágil e métricas

**Projeto:** Linha de injeção e pintura de para-choques · Plásticos Abrantes (G7) · ENGN62 2026.2
**Versão:** 0.1 (rascunho) · **Data de status:** 13/11/2026 · **Responsável:** Guilherme · **Revisão:** ____________
**Fontes:** tabelas 15, 20 a 24, 33, 35 e 37; convenções 8, 9 e 13

## 1. Rotina

Sprints de 2 semanas desde 04/05/2026. Cerimônias: planejamento da sprint, reunião diária, revisão, retrospectiva; status semanal com a gestão. Quadro: A FAZER → EM ANDAMENTO → EM REVISÃO → EM TESTE → CONCLUÍDO.

## 2. Velocidade

| Sprint | Início | Fim | Comprometido | Concluído (pt) |
|---|---|---|---|---|
| S01 | 04/05/2026 | 15/05/2026 | — | 17 |
| S02 | 18/05/2026 | 29/05/2026 | — | 11 |
| S03 | 01/06/2026 | 12/06/2026 | — | 24 |
| S04 | 15/06/2026 | 26/06/2026 | — | 21 |
| S05 | 29/06/2026 | 10/07/2026 | — | 16 |
| S06 | 13/07/2026 | 24/07/2026 | — | 9 |
| S07 | 27/07/2026 | 07/08/2026 | — | 23 |
| S08 | 10/08/2026 | 21/08/2026 | — | 18 |
| S09 | 24/08/2026 | 04/09/2026 | — | 5 |
| S10 | 07/09/2026 | 18/09/2026 | — | 13 |
| S11 | 21/09/2026 | 02/10/2026 | — | 25 |
| S12 | 05/10/2026 | 16/10/2026 | — | 16 |
| S13 | 19/10/2026 | 30/10/2026 | — | 11 |
| S14 | 02/11/2026 | 13/11/2026 | — | 15 |


Média das 5 últimas: **16,0 pt/sprint**.

## 3. Fluxo

| Sprint | Pontos | Velocidade | Ciclo médio (du) | Vazão (itens/du) | WIP (Little) |
|---|---|---|---|---|---|
| S13 | 35 | 11 | 6,17 | 0,60 | 3,7 |
| S14 | 32 | 15 | 7,00 | 0,80 | 5,6 |

Burndown S14 (restantes no fim de cada du): 32, 26, 25, 24, 22, 20, 18, 17, 17.

## 4. DORA, qualidade e equipe

- Implantações em produção: 18 em 27,6 semanas → **0,65/semana**; taxa de falha **44%**; restauração média 4,7 h; lead time mediano 44,1 h (convenção 13).
- Defeitos abertos: 24 no total, 7 sem resolução. Impedimentos: 9, 2 abertos.
- Pulso da equipe: S10=2,81, S11=3,48, S12=4,01, S13=3,79, S14=4,00 (escala 1 a 5).
- Funil do piloto: _(resumir a tabela 37: alcance, ativação, retenção, NPS)_.

**Leitura:** 44% de falha nas implantações e itens entrando no meio da sprint explicam a velocidade instável. Ações: definição de pronto com teste automatizado; proteger a sprint de pedidos diretos.

---
*Rascunho gerado a partir dos números do sistema (https://trabalhodegest-odeprojetos.netlify.app, data de corte 13/11/2026, com os boletins B1 a B10 lançados). O responsável revisa, completa os campos em branco, ajusta o texto e assina.*
