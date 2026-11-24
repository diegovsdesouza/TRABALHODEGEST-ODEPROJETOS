# ProjectLibre · cronograma do G7 (responsável: Caique)

Arquivos: `cronograma_G7.xml` (o projeto) e `avanco_13-11.csv` (o avanço real na data de status). O ProjectLibre roda **no computador** (Windows, Mac ou Linux), não no iPad nem no celular.

1. Instale o ProjectLibre (projectlibre.com, gratuito).
2. **Arquivo → Abrir** → escolha o `cronograma_G7.xml`. Ele traz:
   - o calendário de segunda a sexta, 8 h por dia, com os feriados da tabela 11;
   - a EAP (8 entregas e 22 pacotes) como tarefas-resumo;
   - as 59 atividades com a duração PERT, ⌈(O + 4M + P) ÷ 6⌉;
   - as 88 ligações com tipo (TI = término-início; II = início-início) e defasagem em dias.
3. **Confira antes de seguir:**
   - o término do projeto deve ser **27/04/2027**;
   - a coluna "Crítica" / caminho crítico deve marcar A01 → A07 → A08 → A09 → A11 → A12 → A13 → A38 → A41 → A43 → A44 → A46 → A47 → A49 → A56;
   - se algo diferente aparecer, me avise antes de salvar a linha de base.
4. **Projeto → Linha de base → Salvar linha de base.**
5. Defina a **data de status 13/11/2026** (Projeto → Informações do projeto).
6. Lance o avanço real de cada atividade do `avanco_13-11.csv`: duplo clique na tarefa → **% concluído**, **Início real** e, se tiver, **Término real**.
7. Confira a previsão: o término deve ir para **10/05/2027**.
8. **Salve como `.pod`** em `docs/projectlibre/` e exporte em **PDF** o Gantt (com a linha de base) e a rede (Diagrama de rede) com o caminho crítico.

Observação: o arquivo foi gerado pelo `scripts/exportar_ferramentas.py` no formato XML do MS Project, que o ProjectLibre abre. Se a importação mostrar algum alerta, mande o print.
