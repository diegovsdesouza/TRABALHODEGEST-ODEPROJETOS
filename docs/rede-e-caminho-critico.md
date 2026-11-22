# Rede, caminho crítico e previsão de término — G7 Plásticos Abrantes

**Versão:** 1 · **Data:** 22/11/2026 · **Responsável:** [nome]
**Scripts:**
- `scripts/cpm.py`: linha de base, convenções 1 e 2. Gera `docs/linha_de_base.csv`.
- `scripts/previsao.py`: previsão em 13/11/2026, convenções 8, 10 e 11. Gera `docs/previsao_status.csv`.

**Fontes:**
- Tabelas 07, 08, 11, 14, 17 e 20, já tratadas.
- Boletins B1, B5 e B6 do dossiê.

## 1. Linha de base (convenções 1 e 2)

**Como as durações foram calculadas:**
- Atividade estimada: duração = ⌈(O + 4M + P) ÷ 6⌉.
- Marco ágil: usa `duracao_fixa_du`.

**Como a rede foi montada:**
- Dependência TI: início ≥ término da predecessora + 1 + defasagem.
- Dependência II: início ≥ início da predecessora + defasagem.
- O dia útil 1 é 02/02/2026.

| Item | Resultado |
|---|---|
| Término da linha de base | **du 304 = 27/04/2027** (marco M6, Aceite final) |
| Folga até o término contratual (07/05/2027, du 312) | 8 du |
| Caminho crítico (15 de 59 atividades) | A01 → A07 → A08 → **A09** → A11 → A12 → A13 → A38 → A41 → A43 → A44 → A46 → A47 → A49 → A56 |
| Quase críticas (folga ≤ 5 du) | A55 (folga de 5 du) |
| Marcos da linha de base | M1 Projeto executivo 27/04/2026 · M2 Injetora na fábrica 19/11/2026 · M3 Release 1 10/07/2026 · M4 Montagem concluída 31/12/2026 · M5 SAT 16/03/2027 · M6 Aceite final 27/04/2027 |

**Leitura:** o projeto é comandado pela **cadeia da injetora de 3.200 t**:
- especificação e contratação;
- fabricação de 122 du (A09), a atividade mais longa da rede;
- FAT, transporte e recebimento;
- montagem;
- NR-12, testes a frio, SAT, partida e aceite.

A trilha ágil (A57 a A59) não está no caminho crítico da linha de base.

**Conferência:** o dossiê dá 0,43 mês de atraso para o C1 (término em 10/05/2027). Pela convenção 23, isso equivale a 13 dias corridos ÷ 30,4. Os 13 dias são exatamente o intervalo de 27/04 a 10/05/2027 ✅

## 2. Previsão na data de status, 13/11/2026 (convenção 11)

**Trilha ágil (convenções 8 e 10), com a sprint S14 lançada:**
- Itens e pontos concluídos: 73 itens e 224 pontos, iguais aos números de controle ✅
- Velocidade das sprints S10 a S14: 13, 25, 16, 11 e 15 pontos, com **média de 16,0 pontos por sprint**.
- **Release 2:** faltam 29 pontos, o que dá 2 sprints. Ela fica pronta no fim da S16, em **11/12/2026**. Estava prevista para 02/10/2026: são 47 du de atraso.
- **Release 3:** faltam 90 pontos acumulados, o que dá 6 sprints. Ela fica pronta no fim da S20, em **05/02/2027**. Estava prevista para 24/12/2026: são 29 du de atraso.

**Trilha preditiva, com o boletim B1:**
- A35 e A39 estão concluídas.
- A12 está em 70% e termina em 27/11/2026, contra 13/11 na linha de base.
- A33 está em 90% e termina em 18/11/2026, contra 10/09 na linha de base.

| Item | Resultado |
|---|---|
| **Término previsto** | **du 313 = 10/05/2027**, igual ao C1 do dossiê ✅ |
| Desvio sobre a linha de base | +9 du |
| Além do término contratual | **+1 du**, com custo do atraso de R$ 50.100 |
| Cadeia que define a data hoje | **A12 (transporte e desembaraço da injetora, 70%)** → A13 → A38 → A41 → A43 → A44 → A46 → A47 → A49 → A56 |

**Leitura para o comitê:**
1. **O que define a data é a injetora importada.** O transporte e o desembaraço (A12) começaram 9 du depois do planejado e empurram todo o restante da cadeia em 9 du. A folga de 8 du que existia até o contrato foi consumida, e hoje faltam 1 du.
2. **A elétrica (A33) e a Release 2 estão muito atrasadas, com 47 du cada, mas ainda não definem a data.** Elas têm folga, porque o teste de aceite em campo (A47) só começa em março de 2027. A folga existe, mas está sendo consumida. Se a velocidade do time ágil cair para menos de 16 pontos por sprint, ou se aparecerem novos pedidos diretos, a Release 2 pode entrar no caminho crítico.
3. Qualquer novo atraso na injetora custa R$ 50.100 por dia útil.

## 3. Gabarito de conferência — folhas M1 e M2 (não é a folha; a folha é feita à mão)

**M1, sub-rede de 12 atividades:**

| Ativ. | Dur. (du) | IC | TC | IT | TT | Folga |
|---|---|---|---|---|---|---|
| A32 | 42 | 1 | 42 | 1 | 42 | **0** |
| A33 | 29 | 16 | 44 | 16 | 44 | **0** |
| A34 | 5 | 45 | 49 | 45 | 49 | **0** |
| A35 | 28 | 26 | 53 | 38 | 65 | 12 |
| A38 | 27 | 1 | 27 | 13 | 39 | 12 |
| A39 | 24 | 1 | 24 | 16 | 39 | 15 |
| A40 | 20 | 9 | 28 | 27 | 46 | 18 |
| A41 | 7 | 28 | 34 | 40 | 46 | 12 |
| A42 | 16 | 50 | 65 | 50 | 65 | **0** |
| A43 | 13 | 35 | 47 | 47 | 59 | 12 |
| A44 | 6 | 48 | 53 | 60 | 65 | 12 |
| A46 | 14 | 66 | 79 | 66 | 79 | **0** |

O prazo da sub-rede é **79 du**. O caminho crítico é **A32 → A33 → A34 → A42 → A46**.

Atenção ao A33: ele é **crítico** mesmo ligado ao A32 por II+15. O A34 precisa do término dos dois, e o A33 termina depois (du 44 contra du 42).

**M2, incerteza do prazo:**

| Ativ. crítica | σ = (P − O) ÷ 6 | σ² |
|---|---|---|
| A32 | 4,000 | 16,000 |
| A33 | 2,667 | 7,111 |
| A34 | 0,500 | 0,250 |
| A42 | 1,500 | 2,250 |
| A46 | 2,167 | 4,694 |
| **Caminho** | **σ = √30,306 = 5,505 du** | **30,306** |

- P(T ≤ 79 + 5 = 84 du) = Φ(5 ÷ 5,505) = Φ(0,908) ≈ **81,8%**
- P(T ≤ 79 du) = Φ(0) = **50%**

**Leitura:** prometer a data calculada pela rede é apostar numa moeda, com 50% de chance. Para ter cerca de 82% de confiança, é preciso pedir 5 du a mais, que é o papel da reserva de prazo.
