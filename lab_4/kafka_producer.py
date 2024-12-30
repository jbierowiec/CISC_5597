from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='34.145.215.63:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Starting Producer...")
for i in range(1, 11):
    message = {"id": i, "message": f"External IP Test Message {i}"}
    producer.send("lab-demo", value=message)
    print(f"Sent: {message}")
    time.sleep(1)

producer.close()
print("Producer finished.")
