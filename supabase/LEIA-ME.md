# Instalação do banco no Supabase (10 minutos)

Projeto: `https://chxmmpxnzdbnfnvtjjng.supabase.co` (TrabGP)

## 1. Criar as tabelas e carregar o histórico

No Supabase, abra o **SQL Editor** (ícone `>_` no menu da esquerda) e toque em **New query**. Para **cada arquivo abaixo, nesta ordem**:
1. abra o arquivo no GitHub;
2. toque em **Raw**, selecione tudo e copie;
3. cole no editor e toque em **Run**;
4. espere o "Success" antes de passar para o próximo.

| Ordem | Arquivo | O que faz |
|---|---|---|
| 1 | `01_schema.sql` | Cria as 46 tabelas e as regras de acesso (RLS) |
| 2 | `02_carga_planejamento.sql` | Tabelas 01 a 16: governança, plano preditivo e plano ágil |
| 3 | `03_carga_execucao.sql` | Tabelas 17 a 37: execução tratada até 30/10 (o maior arquivo, cerca de 170 KB) |
| 4 | `04_carga_pessoas_cenarios.sql` | Tabelas 38 a 46: modelo 3D, pessoas e cenários |

Se o editor avisar que a query é "destrutiva" (porque o arquivo 1 apaga e recria as tabelas), confirme: é esperado.

**Conferência imediata.** Rode esta consulta no SQL Editor:

```sql
select (select count(*) from apontamento_horas) as linhas_horas,
       (select sum(horas_normais + horas_extras) from apontamento_horas) as horas,
       (select sum(valor_rs) from custos_realizados) as custos,
       (select count(*) from avanco_semanal) as informes;
```

O resultado esperado é **508 · 11708.5 · 35573360.67 · 259**.

## 2. Login dos integrantes (para lançar os boletins)

No Supabase, vá em **Authentication → Sign In / Providers → Email**:
- deixe o login por e-mail habilitado;
- **desligue "Confirm email"**.

Assim, cada integrante cria a própria conta direto no site, sem precisar confirmar por e-mail. Toda linha lançada pelas telas grava `lancado_por_email`, o que prova a exigência de "pelo menos três pessoas".

## 3. Segurança

- A chave **publicável** fica em `app/js/config.js`. Ela é pública por definição: quem protege os dados é a RLS, em que todos leem e só usuário logado grava.
- A chave **secreta** (service_role) e a senha do banco **nunca** vão para o repositório.

## 4. Regerar os scripts (se os dados tratados mudarem)

```bash
python scripts/build_supabase.py dados/tratados supabase
```
