from kafka import KafkaProducer
import json
import time
import random
from faker import Faker

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

queue_names = ["Payments", "Orders", "Refunds", "Delivery"]

while True:

    call_event = {
        "customer_id": fake.uuid4(),
        "agent_id": random.randint(1000, 2000),
        "queue_name": random.choice(queue_names),
        "call_duration": random.randint(60, 600),
        "wait_time": random.randint(5, 120),
        "sla_breach": random.choice([True, False]),
        "sentiment": random.choice(["positive", "neutral", "negative"]),
        "timestamp": str(fake.date_time())
    }

    producer.send('ivr_calls', call_event)

    print("Sent event to Kafka:")
    print(call_event)

    time.sleep(2)