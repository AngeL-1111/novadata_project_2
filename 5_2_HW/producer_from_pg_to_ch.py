# producer_pg_to_kafka.py
import psycopg2
from kafka import KafkaProducer
import json
import time

def get_unsent_rows(cursor):
    cursor.execute("""
        SELECT id, username, event_type, extract(epoch FROM event_time)
        FROM user_logins
        WHERE sent_to_kafka = FALSE
    """)
    return cursor.fetchall()

def mark_row_as_sent(cursor, row_id):
    cursor.execute("UPDATE user_logins SET sent_to_kafka = TRUE WHERE id = %s", (row_id,))

def main():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    try:
        conn = psycopg2.connect(
            dbname="test_db", user="admin", password="admin", host="localhost", port=5432
        )
        cursor = conn.cursor()

        rows = get_unsent_rows(cursor)

        for row in rows:
            data = {
                "user": row[1],
                "event": row[2],
                "timestamp": float(row[3])
            }

            producer.send("user_events_migration", value=data)
            print("Sent:", data)

            mark_row_as_sent(cursor, row[0])
            conn.commit()
            time.sleep(0.5)

        producer.flush()

    except Exception as e:
        print("Error occurred:", e)

    finally:
        producer.close()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()