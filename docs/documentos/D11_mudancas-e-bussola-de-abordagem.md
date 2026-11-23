# D11 · Mudanças e Bússola de Abordagem

**Projeto:** Linha de injeção e pintura de para-choques · Plásticos Abrantes (G7) · ENGN62 2026.2
**Versão:** 0.1 (rascunho) · **Data de status:** 13/11/2026 · **Responsável:** Guilherme · **Revisão:** ____________
**Fontes:** tabelas 05, 14, 20 e 28 (com o boletim B8)

## 1. Registro de mudanças × matriz de alçadas

| SM | Abertura | Solicitante | Descrição | Tipo | Custo (R$) | Prazo (du) | Pontos | Situação | Decidiu | Alçada exigida |
|---|---|---|---|---|---|---|---|---|---|---|
| SM-001 | 06/04/2026 | PI13 | Antecipar o treinamento para um turno adicional | PRAZO | 61.600 | 3 | 0 | REJEITADA | GERENTE | GERENTE |
| SM-002 | 15/05/2026 | PI13 | Aumentar a capacidade do sistema de exaustão | ESCOPO | 171.400 | 5 | 0 | REJEITADA | GERENTE | PATROCINADOR |
| SM-003 | 21/05/2026 | PI01 | Ampliar a sala elétrica para futura expansão | ESCOPO | 234.200 | 8 | 0 | APROVADA | GERENTE | PATROCINADOR |
| SM-004 | 22/05/2026 | PI05 | Substituir o fornecedor de painéis por marca homologada pelo cliente | TECNICA | 238.300 | 10 | 0 | APROVADA | GERENTE | PATROCINADOR |
| SM-005 | 25/05/2026 | PI01 | Reforçar as bases para um futuro segundo equipamento | ESCOPO | 229.500 | 7 | 0 | APROVADA | PATROCINADOR | PATROCINADOR |
| SM-006 | 01/06/2026 | PI05 | Incluir plataforma de acesso para manutenção do equipamento principal | ESCOPO | 75.200 | 4 | 0 | REJEITADA | GERENTE | PATROCINADOR |
| SM-007 | 02/06/2026 | PI13 | Alterar o layout para ampliar o corredor de empilhadeiras | ESCOPO | 111.300 | 6 | 0 | REJEITADA | GERENTE | PATROCINADOR |
| SM-008 | 18/06/2026 | PI10 | Adicionar redundância na rede de ar comprimido | TECNICA | 159.600 | 5 | 0 | APROVADA | GERENTE | GERENTE |
| SM-009 | 22/06/2026 | PI05 | Trocar a especificação do piso para resina de alta resistência | TECNICA | 192.600 | 5 | 0 | APROVADA | GERENTE | GERENTE |
| SM-010 | 26/08/2026 | PI13 | Enviar relatório automático por e-mail no fim do turno | ESCOPO | 15.100 | 0 | 5 | APROVADA | GERENTE | PATROCINADOR |
| SM-011 | 31/08/2026 | PI13 | Criar indicador de consumo de energia por produto | ESCOPO | 15.100 | 0 | 5 | APROVADA | GERENTE | PATROCINADOR |
| SM-012 | 08/09/2026 | PI02 | Adicionar etiqueta com QR Code por palete | ESCOPO | 24.100 | 0 | 8 | REJEITADA | GERENTE | PATROCINADOR |
| SM-013 | 19/10/2026 | PI13 | Integrar o sistema ao aplicativo corporativo | ESCOPO | 24.100 | 0 | 8 | REJEITADA | GERENTE | PATROCINADOR |
| SM-014 | 11/11/2026 | PI13 | Adicionar sistema de visão para inspeção na linha | ESCOPO | 264.200 | 10 | 0 | EM_ANALISE | — | PATROCINADOR |


Alçadas (tabela 05): GERENTE: até R$ 195.000 e 5 du, escopo NAO; PATROCINADOR: até R$ 780.000 e 15 du, escopo SIM; COMITE: até sem limite e ∞ du, escopo SIM.
**SM-014 (sistema de visão, R$ 264.200 e 10 du)** está em análise e passa da alçada do gerente: vai ao PATROCINADOR.

## 2. Escopo que entrou sem controle

Itens PEDIDO_DIRETO (todos da engenharia da montadora, PI13): PA-163, PA-164, PA-168, PA-170, PA-171, PA-173, PA-189, PA-195 + PA-195 (na S14) = **8 itens, 22 pontos**, sem solicitação de mudança. Custo estimado: 22 × custo real por ponto (R$ 2.949) = R$ 64.886.

## 3. Bússola de Abordagem

| Domínio | Variável que decide | Preditiva quando… | Ágil quando… | No G7 |
|---|---|---|---|---|
| Escopo | estabilidade dos requisitos | o escopo é estável e contratado (equipamentos, obra) | o escopo é incerto e descoberto com o usuário (sistemas) | equipamentos e obra: preditiva; sistemas digitais: ágil |
| Mudança | custo de mudar depois | mudar é caro (concreto, máquina importada) | mudar é barato (software) | mudanças na linha passam pelo comitê; no software, pelo dono do produto, nunca direto |
| Entrega | entrega de uma vez × em partes | só tem valor completa (a linha) | entrega valor em partes (releases) | linha: uma entrega; sistemas: 3 releases |
| Usuário | proximidade do usuário | usuário distante, aceita no fim | usuário perto, revisa a cada sprint | operadores e engenharia da montadora nas revisões |

## 4. Mapa de interfaces entre as trilhas

| Ponto de encontro | Depende de | Prazo hoje | Quem responde |
|---|---|---|---|
| A47 teste de aceite em campo (SAT) | Release 2 (A58) | R2 prevista 11/12/2026; A47 começa em mar/2027 | gerente do projeto + dono do produto |
| A56 aceite final | Release 3 (A59) | R3 prevista 05/02/2027 | gerente do projeto |
| Integração CLP × supervisório (A36/A37) | épico EP01 | _(completar)_ | integrador + time ágil |

---
*Rascunho gerado a partir dos números do sistema (https://trabalhodegest-odeprojetos.netlify.app, data de corte 13/11/2026, com os boletins B1 a B10 lançados). O responsável revisa, completa os campos em branco, ajusta o texto e assina.*
