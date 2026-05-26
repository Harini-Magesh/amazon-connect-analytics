from faker import Faker
import random
import json
import time
from datetime import datetime

fake = Faker()

queues = ["Payments", "Orders", "Returns", "Technical Support"]
sentiments = ["positive", "neutral", "negative"]

while True:
    call_event = {
        "customer_id": f"C{random.randint(1000,9999)}",
        "agent_id": f"A{random.randint(100,999)}",
        "queue_name": random.choice(queues),
        "call_duration": random.randint(60,900),
        "wait_time": random.randint(5,120),
        "sla_breach": random.choice([True, False]),
        "sentiment": random.choice(sentiments),
        "timestamp": datetime.now().isoformat()
    }

    print(json.dumps(call_event, indent=4))

    time.sleep(2)