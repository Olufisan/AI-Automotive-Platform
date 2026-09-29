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
            INSERT INTO automotive_evidence (
                customer_message,
                observation,
                context,
                severity_or_intensity,
                duration,
                confirmed_by_technician
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                "The grinding noise is mild.",
                "The grinding noise is mild.",
                "",
                "mild",
                "",
                False,
            ),
        )

        record_id = cursor.fetchone()[0]

        print(f"Inserted record ID: {record_id}")

        cursor.execute(
            """
            SELECT
                id,
                customer_message,
                observation,
                severity_or_intensity,
                confirmed_by_technician
            FROM automotive_evidence
            WHERE id = %s
            """,
            (record_id,),
        )

        record = cursor.fetchone()

        print("Retrieved record:")
        print(record)