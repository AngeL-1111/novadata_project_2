# consumer_to_clickhouse.py
from kafka import KafkaConsumer
import json
import clickhouse_connect

BATCH_SIZE = 10

def main():
    consumer = KafkaConsumer(
        "user_events_migration",
        bootstrap_servers="localhost:9092",
        group_id="pg_ch_consumer",
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    client = clickhouse_connect.get_client(
        host='localhost',
        port=8123,
        username='user',
        password='strongpassword'
    )

    client.command("""
        CREATE TABLE IF NOT EXISTS user_logins (
            username String,
            event_type String,
            event_time DateTime
        ) ENGINE = MergeTree()
        ORDER BY event_time
    """)

    batch = []

    try:
        for message in consumer:
            data = message.value
            print("Received:", data)

            batch.append((
                data['user'],
                data['event'],
                int(data['timestamp'])  # ClickHouse expects UNIX timestamp as int
            ))

            if len(batch) >= BATCH_SIZE:
                client.insert("user_logins", batch, column_names=["username", "event_type", "event_time"])
                batch.clear()

    except Exception as e:
        print("Error in consumer:", e)

    finally:
        # Insert remaining messages
        if batch:
            client.insert("user_logins", batch, column_names=["username", "event_type", "event_time"])
        consumer.close()

if __name__ == "__main__":
    main()