# Sistema de acompanhamento (Parte 2)

Site estático (HTML + JavaScript, módulos ES, sem etapa de build) que lê e grava no Supabase.

| Arquivo | Função |
|---|---|
| `index.html` | Página única, menu e login |
| `js/config.js` | URL e chave **publicável** do Supabase (a secreta nunca entra aqui) |
| `js/db.js` | Acesso ao banco, cache das 46 tabelas e formatação |
| `js/calc.js` | Núcleo de cálculo: convenções 1 a 23 (rede, previsão, valor agregado, ágil, controle, riscos) |
| `js/telas.js` | R3 · telas de lançamento dos boletins B1 a B10 e do boletim surpresa |
| `js/paginas.js` | R4, R5, R6, R11 e conferência |

**Testes** (pasta `testes/`): `teste_calc.mjs` confere os cálculos com o dossiê; `teste_boletins.py` abre o site num navegador real, lança os 10 boletins pelas telas e confere os 13 números de controle de 13/11 (todos conferem).
