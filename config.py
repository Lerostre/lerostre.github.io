DEV_DB = "'sqlite:///enquete.db'"

pg_user = 'postgres'
pg_pass = 'postgres'
pg_db = 'enquete'
pg_host = 'postgres'
pg_port = 5432

PROD_DB = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'