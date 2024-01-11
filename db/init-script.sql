USE master;
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'maxitransfers')
BEGIN
    CREATE DATABASE maxitransfers;
END;