# D17 · Modelo 3D

**Projeto:** Linha de injeção e pintura de para-choques · Plásticos Abrantes (G7) · ENGN62 2026.2
**Versão:** 0.1 · **Data de status:** 13/11/2026 · **Responsável:** Caique · **Revisão:** Caique Mattos, 24/11/2026
**Fontes:** tabela 38; página Modelo 3D do sistema (R12)

## 1. O modelo

24 elementos da tabela 38 (posição e volume em metros) desenhados no sistema com Three.js: terreno, galpão existente (envoltória transparente), Linha de painéis em operação, e os elementos novos. Cada elemento está ligado a atividades, a um épico ou às releases (campo `vinculo_ids`).

- **Controle de data:** até 13/11/2026 o avanço é o real (tabela 17); depois, a previsão pela rede.
- A altura e a cor sobem com o avanço; o vermelho marca o que está na cadeia do término e atrasado. Tocar num elemento mostra as atividades e o avanço de cada uma.

## 2. Etapas de implantação (ordem pela data de início da linha de base)

| Etapa | Elemento | Nome | Ligado a | Início na linha de base |
|---|---|---|---|---|
| 1 | EL09 | Injetora de 3.200 t | A09;A12;A13;A38;A41 | 30/03/2026 |
| 2 | EL10 | Cabine de pintura robotizada | A16;A19;A20;A39;A41 | 02/04/2026 |
| 3 | EL22 | Sala de treinamento | A51;A52;A53 | 02/04/2026 |
| 4 | EL11 | Transportador aéreo e robôs de manipulação | A22;A23;A40 | 09/04/2026 |
| 5 | EL04 | Canteiro e tapume de isolamento | A24 | 28/04/2026 |
| 6 | EL14 | Sala elétrica e painéis de força | A32;A33;A34;A42 | 28/04/2026 |
| 7 | EL15 | Rede industrial e instrumentação | A35;A36;A37 | 14/08/2026 |
| 8 | EL05 | Bases dos equipamentos | A25;A26 | 12/05/2026 |
| 9 | EL07 | Adequação predial (cobertura e exaustão) | A30 | 19/05/2026 |
| 10 | EL13 | Utilidades: água gelada, ar comprimido e tratamento de efluentes | A28;A29 | 26/05/2026 |
| 11 | EL08 | Rede de combate a incêndio | A31 | 29/05/2026 |
| 12 | EL06 | Piso industrial e canaletas | A27 | 29/06/2026 |
| 13 | EL12 | Proteções e enclausuramento (NR-12) | A43;A44 | 12/01/2027 |
| 14 | EL23 | Almoxarifado de sobressalentes | A54 | 10/02/2027 |
| 15 | EL24 | Doca e área de testes com produto | A46;A47;A48;A49 | 10/02/2027 |
| 16 | EL16 | Sala de controle (sistemas digitais) | R1;R2;R3 | trilha ágil |
| 17 | EL17 | Módulo: Coleta de dados da linha | EP01 | trilha ágil |
| 18 | EL18 | Módulo: Painel de desempenho e paradas | EP02 | trilha ágil |
| 19 | EL19 | Módulo: Rastreabilidade de lotes e qualidade | EP03 | trilha ágil |
| 20 | EL20 | Módulo: Receitas, setup e ordens de produção | EP04 | trilha ágil |
| 21 | EL21 | Módulo: Manutenção e treinamento digital | EP05 | trilha ágil |


**Ordem de implantação proposta (campo `ordem_de_implantacao`):** a ordem acima. **Justificativa:** segue a lógica física da obra e as dependências da rede: primeiro o que fica embaixo e em volta (área, bases, piso e utilidades), depois a elétrica que alimenta os equipamentos, então os equipamentos na sequência do caminho crítico (injetora antes da cabine e do transportador), as proteções NR-12 e, por fim, as áreas de apoio e testes. A sala de controle e os módulos digitais seguem as releases da trilha ágil, em paralelo.

**Capturas da animação (página Modelo 3D):** projeto executivo, obra civil pronta, equipamentos montados e linha pronta, em `docs/` (anexadas pelo responsável).

