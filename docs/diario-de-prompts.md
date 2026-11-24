# Diário de prompts · G7 · Plásticos Abrantes

Regra do enunciado: **10 entradas, de pelo menos 3 pessoas**. Regra do grupo: **cada um escreve pelo menos 2**. Cada entrada responde: o que pedimos, o que a IA errou e como corrigimos (e como percebemos o erro).

| # | Data | Quem | Ferramenta | O que pedimos | O que a IA errou | Como percebemos e corrigimos |
|---|---|---|---|---|---|---|
| 1 | 22/11 | Diego | Claude | Criar as 46 tabelas no Supabase com colunas de controle para separar o histórico do que é lançado pelas telas | Deu à coluna de controle o nome `origem`, que já existia no backlog (tabela 14) com outro significado | A carga do backlog falhou; renomeamos a coluna de controle para `fonte_registro` em todas as tabelas |
| 2 | 22/11 | Diego | Claude | Gerar os rascunhos dos documentos D1 a D17 com os números do sistema | Leu os CSVs do histórico (até 30/10) e ignorou os boletins de 03 a 13/11 | Os números não batiam com a página Conferência; o gerador passou a ler do banco, com os boletins lançados |
| 3 | 22/11 | Diego | Claude | Mostrar no dashboard se a reserva de contingência cobre os riscos | O indicador dizia "cobre 100%" com a contingência já estourada | Conferimos contra o D9: saldo de −R$ 266.400; o indicador passou a mostrar o saldo |
| 4 | 22/11 | Diego | Claude | Ligar o assistente de IA do sistema ao Gemini | Sem a chave configurada, a tela mostrava "IA (undefined)" em vez de cair na resposta local | Testamos sem a chave; a tela só aceita a resposta da IA quando ela existe |
| 5 | | Caique | | | | |
| 6 | | Caique | | | | |
| 7 | | José | | | | |
| 8 | | José | | | | |
| 9 | | Marjorie | | | | |
| 10 | | Marjorie | | | | |
| 11 | 22/11 | Guilherme | Claude | Configurar o quadro do Jira com as colunas Em revisão e Em teste, que o fluxo da base de dados usa e o quadro padrão do Scrum não tem | Passou o caminho de um menu que não existe na versão atual do Jira (criar a coluna pelo campo "Colunas" das configurações do projeto) | Ao seguir o passo a passo, o menu não apareceu na tela; enviamos prints e o caminho foi corrigido: os status são criados no editor de fluxo de trabalho ("Adicionar status") e as colunas em Configurar colunas, no menu do quadro. Registramos nos pontos de atenção que os status foram criados depois da carga e que as transições anteriores não ficaram no histórico do Jira |
| 12 | 22/11 | Guilherme | Claude | Redigir o D7 (backlog e releases no Jira) a partir dos dados e do que foi montado no Jira | Incluiu no documento exigências que a especificação do D7 não pede, apresentadas como se fizessem parte dela | Na revisão, comparamos o texto com a especificação do D7 no kit e perguntamos de onde vinham aqueles itens; a IA confirmou que eram proposta dela. Cortamos o que não fazia parte da entrega e o documento ficou com 4 páginas |
| 13 | | Arley | | | | |
| 14 | | Arley | | | | |

**Dica para preencher:** vale qualquer conversa com IA usada no trabalho (folhas, documentos, Jira, ProjectLibre, slides). O que conta é o erro concreto e a conferência que vocês fizeram, por exemplo: "a IA calculou o PERT sem arredondar para cima; conferimos com a convenção 1 do dicionário".
