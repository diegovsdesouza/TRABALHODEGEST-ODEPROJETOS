# D4 · Cronograma (ProjectLibre)

**Projeto:** Linha de injeção e pintura de para-choques · Plásticos Abrantes (G7) · ENGN62 2026.2
**Versão:** 1.0 · **Data de status:** 13/11/2026 · **Responsável:** Caique · **Revisão:** Caique Mattos, 24/11/2026
**Fontes:** tabelas 07, 08, 11 e 17; convenções 1, 2 e 11; arquivos docs/projectlibre/

## 1. Como foi montado

1. Calendário de segunda a sexta, 8 h/dia, com os feriados da tabela 11.
2. EAP como tarefas-resumo; as 59 atividades dentro dos pacotes.
3. Duração = ⌈(O + 4M + P) ÷ 6⌉ (convenção 1); marcos ágeis com duração fixa.
4. 88 ligações: TI = término-início (FS), II = início-início (SS), com defasagem em dias úteis (convenção 2).
5. Linha de base salva; avanço real lançado na data de status 13/11/2026.

Arquivos: `cronograma_G7.xml` (projeto gerado), `cronograma_G7.pod` e `gantt_G7.pdf` em `docs/projectlibre/`.

## 2. Resultado

| Item | Linha de base | Previsão em 13/11 |
|---|---|---|
| Término | 27/04/2027 (du 304) | **10/05/2027** (du 313) |
| Folga até o contrato (07/05/2027) | 8 du | **−1 du** (custo R$ 50.100) |
| Caminho crítico / cadeia do término | A01 → A07 → A08 → A09 → A11 → A12 → A13 → A38 → A41 → A43 → A44 → A46 → A47 → A49 → A56 | A11 → A12 → A13 → A38 → A41 → A43 → A44 → A46 → A47 → A49 → A56 |

**Conferência com o sistema e com o papel:** o término e o caminho crítico do ProjectLibre devem ser os mesmos do sistema (página Prazo) e da folha M1 (sub-rede).

**No ProjectLibre** (`cronograma_G7.pod`, `gantt_G7.pdf` e `rede_G7.pdf`): com o avanço de 13/11 lançado, o término previsto ficou em **11/05/2027**, pela mesma cadeia A11 → A12 → A13 → A38 → … → A56. O sistema e a folha M1 dão **10/05/2027**. A diferença de 1 dia útil vem da A12 (transporte da injetora, 70%): o ProjectLibre mantém a duração original a partir do início real (20/10/2026) e termina a A12 em 30/11; a convenção 11 do dicionário reprograma o restante a partir da data de status (13/11 + 28 × 30% = 9 du) e termina em 27/11. Para a decisão vale a convenção 11 (10/05/2027); nos dois casos o projeto passa do contrato (07/05/2027).

## 3. Tabela da rede

| Ativ. | Nome | Dur. | Início LB | Término LB | Folga | Crítica | Situação | Término previsto | Desvio (du) |
|---|---|---|---|---|---|---|---|---|---|
| A01 | Elaborar o projeto básico e o layout da linha | 21 | 02/02/2026 | 04/03/2026 | 0 | sim | concluida | 09/03/2026 | 3 |
| A05 | Obter as licenças e aprovações (ambiental e bombeiros) | 51 | 18/02/2026 | 04/05/2026 | 99 |  | concluida | 11/05/2026 | 5 |
| A02 | Elaborar o projeto executivo civil e de utilidades | 27 | 05/03/2026 | 13/04/2026 | 79 |  | concluida | 14/04/2026 | 1 |
| A03 | Elaborar o projeto executivo elétrico e de automação | 29 | 05/03/2026 | 15/04/2026 | 77 |  | concluida | 22/04/2026 | 4 |
| A07 | Elaborar a especificação técnica: Injetora de 3.200 t | 9 | 05/03/2026 | 17/03/2026 | 0 | sim | concluida | 23/03/2026 | 4 |
| A14 | Elaborar a especificação técnica: Cabine de pintura robotizada | 11 | 05/03/2026 | 19/03/2026 | 33 |  | concluida | 27/03/2026 | 6 |
| A21 | Especificar e contratar: Transportador aéreo e robôs de manipulação | 19 | 12/03/2026 | 08/04/2026 | 83 |  | concluida | 17/04/2026 | 7 |
| A08 | Contratar o fornecimento: Injetora de 3.200 t | 8 | 18/03/2026 | 27/03/2026 | 0 | sim | concluida | 07/04/2026 | 6 |
| A15 | Contratar o fornecimento: Cabine de pintura robotizada | 9 | 20/03/2026 | 01/04/2026 | 33 |  | concluida | 13/04/2026 | 7 |
| A06 | Realizar a análise de risco NR-12 do projeto | 14 | 23/03/2026 | 10/04/2026 | 185 |  | concluida | 06/05/2026 | 16 |
| A09 | Fabricar: Injetora de 3.200 t | 122 | 30/03/2026 | 24/09/2026 | 0 | sim | concluida | 08/10/2026 | 10 |
| A10 | Aprovar os desenhos de fabricação e de bases: Injetora de 3.200 t | 11 | 30/03/2026 | 14/04/2026 | 105 |  | concluida | 27/04/2026 | 8 |
| A16 | Fabricar: Cabine de pintura robotizada | 108 | 02/04/2026 | 09/09/2026 | 33 |  | concluida | 09/09/2026 | 0 |
| A17 | Aprovar os desenhos de fabricação e de bases: Cabine de pintura robotizada | 11 | 02/04/2026 | 17/04/2026 | 102 |  | concluida | 30/04/2026 | 8 |
| A51 | Elaborar o plano de treinamento e os materiais | 16 | 02/04/2026 | 27/04/2026 | 203 |  | concluida | 06/05/2026 | 6 |
| A22 | Fabricar e entregar: Transportador aéreo e robôs de manipulação | 80 | 09/04/2026 | 05/08/2026 | 83 |  | concluida | 17/09/2026 | 30 |
| A04 | Compatibilizar os projetos e emitir para construção | 7 | 16/04/2026 | 27/04/2026 | 77 |  | concluida | 04/05/2026 | 4 |
| A24 | Mobilizar o canteiro e isolar a área em relação à Linha de painéis | 9 | 28/04/2026 | 11/05/2026 | 77 |  | concluida | 15/05/2026 | 4 |
| A32 | Fabricar e instalar os painéis de força e a subestação | 42 | 28/04/2026 | 29/06/2026 | 129 |  | concluida | 28/08/2026 | 43 |
| A52 | Elaborar os procedimentos operacionais padrão | 16 | 28/04/2026 | 20/05/2026 | 203 |  | concluida | 28/05/2026 | 6 |
| A36 | Programar os CLPs e o supervisório | 42 | 04/05/2026 | 03/07/2026 | 140 |  | concluida | 28/07/2026 | 17 |
| A57 | Desenvolver até a Release 1 (MVP) — sprints 1 a 5 | 47 | 04/05/2026 | 10/07/2026 | 76 |  | concluida | 07/08/2026 | 20 |
| A50 | Recrutar e contratar os operadores da nova linha | 31 | 05/05/2026 | 17/06/2026 | 168 |  | concluida | 22/06/2026 | 3 |
| A45 | Elaborar os procedimentos de comissionamento e partida | 11 | 11/05/2026 | 25/05/2026 | 175 |  | concluida | 01/06/2026 | 5 |
| A25 | Demolir o piso existente e escavar as bases | 11 | 12/05/2026 | 26/05/2026 | 77 |  | concluida | 01/06/2026 | 4 |
| A30 | Adequar o prédio (cobertura, exaustão e iluminação) | 26 | 19/05/2026 | 25/06/2026 | 156 |  | concluida | 08/07/2026 | 8 |
| A28 | Instalar as redes de utilidades: água gelada, ar comprimido e tratamento de efluentes | 38 | 26/05/2026 | 21/07/2026 | 131 |  | concluida | 11/08/2026 | 15 |
| A26 | Executar as bases dos equipamentos | 21 | 27/05/2026 | 26/06/2026 | 77 |  | concluida | 29/07/2026 | 22 |
| A31 | Instalar a rede de combate a incêndio da área | 16 | 29/05/2026 | 22/06/2026 | 156 |  | concluida | 06/07/2026 | 8 |
| A27 | Executar o piso industrial e as canaletas | 23 | 29/06/2026 | 30/07/2026 | 77 |  | concluida | 11/09/2026 | 30 |
| A37 | Testar a lógica dos CLPs em bancada | 9 | 06/07/2026 | 16/07/2026 | 140 |  | concluida | 11/08/2026 | 18 |
| A58 | Desenvolver até a Release 2 — sprints 6 a 11 | 59 | 13/07/2026 | 02/10/2026 | 76 |  | prevista pela release | 11/12/2026 | 47 |
| A29 | Testar e liberar as redes de utilidades | 6 | 22/07/2026 | 29/07/2026 | 131 |  | concluida | 20/08/2026 | 16 |
| A33 | Instalar a infraestrutura elétrica e lançar os cabos | 29 | 31/07/2026 | 10/09/2026 | 80 |  | em andamento | 18/11/2026 | 47 |
| A23 | Receber e inspecionar na fábrica: Transportador aéreo e robôs de manipulação | 4 | 06/08/2026 | 11/08/2026 | 83 |  | concluida | 22/09/2026 | 29 |
| A35 | Instalar a instrumentação e a rede industrial | 28 | 14/08/2026 | 23/09/2026 | 92 |  | concluida | 09/11/2026 | 31 |
| A18 | Realizar o teste de aceite em fábrica (FAT): Cabine de pintura robotizada | 6 | 10/09/2026 | 17/09/2026 | 33 |  | concluida | 17/09/2026 | 0 |
| A34 | Energizar os painéis e testar a alimentação | 5 | 11/09/2026 | 17/09/2026 | 80 |  | nao iniciada | 26/11/2026 | 47 |
| A19 | Transportar e descarregar: Cabine de pintura robotizada | 9 | 18/09/2026 | 30/09/2026 | 33 |  | concluida | 29/09/2026 | -1 |
| A11 | Realizar o teste de aceite em fábrica (FAT): Injetora de 3.200 t | 6 | 25/09/2026 | 02/10/2026 | 0 | sim | concluida | 19/10/2026 | 10 |
| A20 | Receber e inspecionar na fábrica: Cabine de pintura robotizada | 4 | 01/10/2026 | 06/10/2026 | 33 |  | concluida | 06/10/2026 | 0 |
| A12 | Transportar e desembaraçar: Injetora de 3.200 t | 28 | 05/10/2026 | 13/11/2026 | 0 | sim | em andamento | 27/11/2026 | 9 |
| A59 | Desenvolver até a Release 3 — sprints 12 a 17 | 56 | 05/10/2026 | 24/12/2026 | 76 |  | prevista pela release | 05/02/2027 | 29 |
| A39 | Montar: Cabine de pintura robotizada | 24 | 07/10/2026 | 11/11/2026 | 33 |  | concluida | 10/11/2026 | -1 |
| A13 | Receber e inspecionar na fábrica: Injetora de 3.200 t | 4 | 16/11/2026 | 19/11/2026 | 0 | sim | nao iniciada | 03/12/2026 | 9 |
| A38 | Montar: Injetora de 3.200 t | 27 | 23/11/2026 | 30/12/2026 | 0 | sim | nao iniciada | 13/01/2027 | 9 |
| A40 | Montar e interligar: Transportador aéreo e robôs de manipulação | 20 | 03/12/2026 | 31/12/2026 | 6 |  | nao iniciada | 14/01/2027 | 9 |
| A41 | Alinhar e nivelar os equipamentos | 7 | 31/12/2026 | 11/01/2027 | 0 | sim | nao iniciada | 22/01/2027 | 9 |
| A42 | Interligar eletricamente os equipamentos | 16 | 31/12/2026 | 22/01/2027 | 10 |  | nao iniciada | 04/02/2027 | 9 |
| A53 | Treinar os operadores e a equipe de manutenção | 16 | 04/01/2027 | 25/01/2027 | 34 |  | nao iniciada | 05/02/2027 | 9 |
| A43 | Instalar as proteções e adequar a linha à NR-12 | 13 | 12/01/2027 | 28/01/2027 | 0 | sim | nao iniciada | 12/02/2027 | 9 |
| A44 | Emitir o laudo de conformidade com a NR-12 | 6 | 29/01/2027 | 05/02/2027 | 0 | sim | nao iniciada | 22/02/2027 | 9 |
| A46 | Executar os testes a frio (sem produto) | 14 | 10/02/2027 | 01/03/2027 | 0 | sim | nao iniciada | 12/03/2027 | 9 |
| A54 | Organizar os sobressalentes, os planos de manutenção e o data book | 16 | 10/02/2027 | 03/03/2027 | 31 |  | nao iniciada | 16/03/2027 | 9 |
| A47 | Executar o teste de aceite em campo (SAT) com produto | 11 | 02/03/2027 | 16/03/2027 | 0 | sim | nao iniciada | 30/03/2027 | 9 |
| A48 | Corrigir as pendências do teste de aceite | 9 | 17/03/2027 | 30/03/2027 | 13 |  | nao iniciada | 12/04/2027 | 9 |
| A49 | Conduzir a partida assistida e a curva de ramp-up | 22 | 17/03/2027 | 16/04/2027 | 0 | sim | nao iniciada | 30/04/2027 | 9 |
| A55 | Registrar as lições aprendidas e desmobilizar o canteiro | 7 | 01/04/2027 | 09/04/2027 | 5 |  | nao iniciada | 23/04/2027 | 9 |
| A56 | Formalizar o aceite final e encerrar o projeto | 6 | 19/04/2027 | 27/04/2027 | 0 | sim | nao iniciada | 10/05/2027 | 9 |
