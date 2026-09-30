import os

import psycopg



def check_database_connection():
      with psycopg.connect(
         host=os.environ["DB_HOST"],
         port=os.environ["DB_PORT"],
         dbname=os.environ["DB_NAME"],
          user=os.environ["DB_USER"],
         password=os.environ["DB_PASSWORD"],
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")

            return True

def save_evidence(customer_message, evidence):
    with psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
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
                    customer_message,
                    evidence.observation,
                    evidence.context,
                    evidence.severity_or_intensity,
                    evidence.duration,
                    evidence.confirmed_by_technician,
                ),
            )

            record_id = cursor.fetchone()[0]

        connection.commit()

    return record_id