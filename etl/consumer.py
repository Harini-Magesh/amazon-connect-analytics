from kafka import KafkaConsumer
import json
import pandas as pd
from sqlalchemy import create_engine

consumer = KafkaConsumer(
    'ivr_calls',
    bootstrap_servers='127.0.0.1:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

engine = create_engine(
    "postgresql://postgres:Harinimagesh%40123@127.0.0.1:5433/postgres"
)

records = []

for message in consumer:

    data = message.value

    print("\nReceived Event:")
    print(data)

    records.append(data)

    if len(records) >= 5:

        df = pd.DataFrame(records)

        df.to_sql(
            'call_records',
            engine,
            if_exists='append',
            index=False
        )

        print("\nInserted 5 records into PostgreSQL")

        records = []