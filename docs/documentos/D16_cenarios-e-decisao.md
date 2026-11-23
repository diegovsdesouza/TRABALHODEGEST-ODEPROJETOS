# D16 · Cenários e decisão

**Projeto:** Linha de injeção e pintura de para-choques · Plásticos Abrantes (G7) · ENGN62 2026.2
**Versão:** 1.0 · **Data de status:** 13/11/2026 · **Responsável:** Diego · **Revisão:** Diego Santana de Souza, 23/11/2026
**Fontes:** tabelas 02 e 43 a 46; convenções 21 a 23; página Cenários; folha M7

## 1. Os seis cenários (convenções 21 a 23)

| Cenário | Nome | Término | du além | ENT (R$) | VPL (R$) | Payback | Custo do atraso | Resultado = VPL − atraso | vs. C1 |
|---|---|---|---|---|---|---|---|---|---|
| C1 | Seguir como está | 10/05/2027 | 1 | 41.764.252 | 3.090.341 | 4,26 | 50.100 | **3.040.241** | 0 |
| C2 | Recuperar o prazo | 14/04/2027 | -16 | 42.896.148 | 2.340.813 | 4,32 | 0 | **2.340.813** | -699.428 |
| C3 | Cortar escopo | 10/05/2027 | 1 | 41.389.882 | 2.321.574 | 4,32 | 50.100 | **2.271.474** | -768.767 |
| C4 | Ampliar o escopo | 23/06/2027 | 32 | 42.969.789 | 4.121.965 | 4,21 | 1.603.200 | **2.518.765** | -521.476 |
| C5 | Trocar a solução | 10/05/2027 | 1 | 41.750.861 | 3.029.234 | 4,27 | 50.100 | **2.979.134** | -61.107 |
| C6 | Partir em dois estágios | 10/05/2027 | 1 | 41.880.652 | 3.388.663 | 4,24 | 50.100 | **3.338.563** | 298.322 |


Conferência com o dossiê (M7): C1 10/05/2027 e ENT 41.764.252; C3 10/05/2027 e 41.389.882; C4 23/06/2027 e 42.969.789 ✔.

## 2. Combinações permitidas (coluna "combinável com" da tabela 43)

| Combinação | Término | du além | ENT | VPL | Resultado | vs. C1 |
|---|---|---|---|---|---|---|
| C2 + C3 | 14/04/2027 | -16 | 42.521.778 | 1.560.883 | **1.560.883** | -1.479.358 |
| C2 + C5 | 14/04/2027 | -16 | 42.882.757 | 2.278.611 | **2.278.611** | -761.630 |
| C2 + C6 | 14/04/2027 | -16 | 43.012.548 | 2.612.663 | **2.612.663** | -427.578 |
| C3 + C6 | 10/05/2027 | 1 | 41.506.282 | 2.607.789 | **2.557.689** | -482.552 |
| C5 + C6 | 10/05/2027 | 1 | 41.867.261 | 3.326.369 | **3.276.269** | 236.028 |

**Combinação testada: C5 + C6.** É a melhor das cinco combinações (R$ 3.276.269, R$ 236.028 acima do C1), mas fica R$ 62.294 abaixo do C6 sozinho: o custo da licença do C5 come o ganho. A combinação não compensa.


## 3. O que se perde em cada escolha

- **C1 seguir como está:** termina 1 du além do contrato (R$ 50.100), com a contingência já estourada (saldo −R$ 266.400) e R$ 371 mil em multas a cobrar. Não resolve nenhum dos problemas do diagnóstico.
- **C2 recuperar o prazo:** termina antes do contrato, mas a compressão custa mais do que o atraso que evita.
- **C3 cortar escopo:** economiza custo, mas perde benefício (−1,4%) e eleva o custo operacional.
- **C4 ampliar o escopo:** maior VPL, mas 32 du de atraso (R$ 1,6 mi) derrubam o resultado.
- **C5 trocar a solução:** perde o que já foi gasto no épico Receitas, setup e ordens de produção (não volta) e acrescenta a licença anual (+R$ 17.500/ano de operação). Fica R$ 61.107 abaixo do C1 e cria dependência de fornecedor.
- **C6 dois estágios:** antecipa 60% do benefício (produção em um turno após os testes a frio) sem mexer no caminho crítico. **Perde:** exige a atividade nova N05 (8 du, R$ 116.400); nos primeiros meses a linha roda em um turno, com operação manual e mais risco de qualidade; o aceite final não antecipa.

## 4. Recomendação ao comitê

**Aprovar o C6 (Partir em dois estágios)**: resultado de R$ 3.338.563, R$ 298.322 acima de seguir como está. Nenhuma combinação supera o C6 sozinho.
**Decisão pedida:** aprovar o investimento adicional e a operação em um turno após os testes a frio · **dono:** gerente do projeto · **prazo:** comitê de dezembro/2026.
Em paralelo (sem custo): bloquear pedidos diretos (D11), cobrar multas (D10) e pedir o remanejamento da reserva gerencial (D9).

