#!/bin/sh
# Recarrega o banco local de teste com o histórico (apaga os lançamentos feitos pelas telas).
for f in supabase/01_schema.sql supabase/02_carga_planejamento.sql supabase/03_carga_execucao.sql supabase/04_carga_pessoas_cenarios.sql; do
  psql -h /tmp/pgt -p 5499 -U postgres -q -v ON_ERROR_STOP=1 -f "$f" >/dev/null 2>&1 || echo "falhou $f"; done
