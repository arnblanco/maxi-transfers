#!/bin/bash
set -e

# Iniciar el servidor SQL
/opt/mssql/bin/sqlservr &

# Esperar a que el servidor SQL esté listo
until /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P MaxiTransfers2023 -d master -Q "SELECT 1" &> /dev/null; do
  echo "Waiting for SQL Server to be ready..."
  sleep 1
done

# Ejecutar el script de inicialización
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P MaxiTransfers2023 -d master -i init-script.sql &&
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P MaxiTransfers2023 -d master -i init-tables.sql &&
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P MaxiTransfers2023 -d master -i init-procedures.sql &&

# Mantener el contenedor en ejecución
tail -f /dev/null

