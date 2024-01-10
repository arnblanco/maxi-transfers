#!/bin/bash
set -e

echo "Se inicio el script"
if [ "$1" = '/opt/mssql/bin/sqlservr' ]; then
  echo "Se ingreso a la primera verificacion"
  if [ ! -f /tmp/app-initialized ]; then
    echo "Se ingreso a la segunda verificacion"
    initialize_app_database() {
      echo "Se inicio la funcion para transfeir el script"
      sleep 15s
      /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P MaxiTransfers2023 -d master -i init-script.sql
      touch /tmp/app-initialized
    }
    initialize_app_database &
  fi
fi

exec "$@"
