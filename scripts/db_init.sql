-- Init script for DB container.

CREATE DATABASE db_nott;
CREATE ROLE pguser LOGIN PASSWORD '123';
GRANT ALL PRIVILEGES ON DATABASE db_nott TO pguser;
