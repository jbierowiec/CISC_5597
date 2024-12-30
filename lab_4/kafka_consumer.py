from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "lab-demo",
    bootstrap_servers='34.145.215.63:29092',
    group_id="external-test-group",
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("Kafka Consumer listening to 'lab-demo'...")
for message in consumer:
    print(f"Received: {message.value}")
