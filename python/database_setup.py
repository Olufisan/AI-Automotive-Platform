import psycopg


with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="automotive",
    user="n8n",
    password="n8npassword",
) as connection:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS automotive_evidence (
                id SERIAL PRIMARY KEY,
                customer_message TEXT NOT NULL,
                observation TEXT NOT NULL,
                context TEXT NOT NULL,
                severity_or_intensity TEXT NOT NULL,
                duration TEXT NOT NULL,
                confirmed_by_technician BOOLEAN NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    connection.commit()

print("Automotive evidence table created successfully")