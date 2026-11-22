# Sala de Guerra das Duas Trilhas · G7 Plásticos Abrantes

Trabalho final de **ENGN62 · Gestão de Projetos** (UFBA, 2026.2, Prof. Lucas Magalhães).
O grupo assume o escritório de projetos da implantação da **linha de injeção e pintura de para-choques** da Plásticos Abrantes, em Camaçari/BA. O projeto é híbrido: trilha preditiva no ProjectLibre e trilha ágil no Jira.

- **Data de status:** 13/11/2026 · **Entrega digital:** 24/11/2026, 23h59
- **Sistema publicado:** _[link da Vercel/Netlify]_
- **Jira:** _[link]_ · **Integrantes:** Diego (coordenação), Caique, Marjorie, José, Guilherme e Arley

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `CONTEXTO.md` | Resumo do caso, regras, convenções e status. **Toda conversa com a IA começa por ele** |
| `dados/brutos/` | As 46 tabelas originais do pacote do G7 |
| `dados/tratados/` | As mesmas tabelas após o tratamento (ver `docs/qualidade-dos-dados.md`) |
| `dados/DICIONARIO.md` | Dicionário de dados e as 23 convenções oficiais de cálculo |
| `scripts/` | `tratamento_dados.py` (limpeza), `cpm.py` (linha de base), `previsao.py` (previsão na data de status) |
| `docs/` | Documentos D1 a D17, qualidade dos dados, diário de prompts, caderno escaneado |

## Números de controle (seção 3 do dossiê)

| Conferência | Esperado (até 30/10) | Obtido |
|---|---|---|
| Horas apontadas, tab. 18 | 11.708,5 | 11.708,5 ✅ |
| Linhas de apontamento, tab. 18 | 508 | 508 ✅ |
| Custos lançados, tab. 19 | R$ 35.573.360,67 | R$ 35.573.360,67 ✅ |
| Custos da preditiva, tab. 19 | R$ 34.632.983,98 | R$ 34.632.983,98 ✅ |
| Lançamentos de custo, tab. 19 | 142 | 142 ✅ |
| Itens no backlog / concluídos / pontos, tab. 14 | 94 / 65 / 209 | 94 / 65 / 209 ✅ |
| Transições, tab. 21 | 297 | 297 ✅ |
| Informes de avanço, tab. 17 | 259 | 259 ✅ |
| Homens-hora / linhas, tab. 42 | 15.860 / 57 | 15.860 / 57 ✅ |
| Custo mensal da folha, tab. 39 | R$ 282.910,40 | R$ 282.910,40 ✅ |

Os números após a quinzena de campo (até 13/11) serão conferidos no sistema, depois do lançamento dos boletins pelas telas.
