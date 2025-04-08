import json
from confluent_kafka import Consumer
import psycopg2

def consume_and_store():
    bootstrap_servers = "localhost"
    topic = "Netflix_adapt"
    group_id = "test-group"

    consumer = Consumer({
        "bootstrap.servers": bootstrap_servers,
        "group.id": group_id,
        "auto.offset.reset": "earliest"
    })

    consumer.subscribe([topic])

    conn = psycopg2.connect(dbname="netflix",
                                user="postgres",
                                password="8888",
                                host="localhost",
                                port="5432")
    cursor = conn.cursor()

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer erreur: {msg.error()}")
            continue

        message_value = msg.value().decode('utf-8')
        print(f"Message reçu: {message_value}")

        if not message_value:
            print("Message reçu vide. Skipping...")
            continue

        try:
            result = json.loads(message_value)
            comment = result['comment']
            sentiment = result['sentiment']

            cursor.execute("INSERT INTO sentiment_table (comment, sentiment) VALUES (%s, %s)", (comment, sentiment))
            conn.commit()
            print("Comment and sentiment stockés dans PostgreSQL.✅")
        except json.JSONDecodeError as e:
            print(f"JSON decode erreur: {e}. Skipping...")

    cursor.close()
    conn.close()
    consumer.close()

consume_and_store()
