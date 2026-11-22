#!/bin/sh
# Liga o Postgres local de teste (se já existir o diretório, só inicia; senão cria, inicia e carrega o histórico).
P=/usr/lib/postgresql/16/bin
if [ ! -d /tmp/pgt/data ]; then
  mkdir -p /tmp/pgt && chown postgres /tmp/pgt
  su postgres -s /bin/sh -c "$P/initdb -D /tmp/pgt/data -A trust >/dev/null"
  NOVO=1
fi
su postgres -s /bin/sh -c "$P/pg_ctl -D /tmp/pgt/data -o '-k /tmp/pgt -p 5499' -l /tmp/pgt/log start" >/dev/null 2>&1
sleep 2
if [ -n "$NOVO" ]; then psql -h /tmp/pgt -p 5499 -U postgres -q -f "$(dirname "$0")/00_stub_local.sql" >/dev/null; sh "$(dirname "$0")/recarregar.sh"; fi
psql -h /tmp/pgt -p 5499 -U postgres -tAc "select 'informes', count(*) from avanco_semanal"
