import psycopg


with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="automotive",
    user="n8n",
    password="n8npassword",
) as connection:
    print("PostgreSQL connection successful")