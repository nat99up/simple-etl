from airflow import DAG
from airflow.operators.python import PythonOperator
import datetime
import json

default_args = {
    'owner': 'airflow',
    'start_date': datetime.datetime(2024, 1, 1),
    'concurrency': 1,
    'schedule_interval': '@once'
}

dag = DAG(
    'kafka_consumer',
    default_args=default_args,
    max_active_runs=1
)

def print_event(topic, event):
    print(f"topic: {topic}")
    print(f"event: {event}")

def listen_kafka():
    from kafka import KafkaConsumer

    consumer = KafkaConsumer(
        bootstrap_servers=['kafka-0:9092', 'kafka-1:9092'],
        group_id='airflow-consumer',
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )
    consumer.subscribe(['ad_event', 'bot_event'])

    for message in consumer:
        topic = message.topic
        event = message.value.decode('utf-8')
        print_event(topic, event)
        event_dict = json.loads(event)

        if topic == 'ad_event':
            print(f"Got ad_event: {event_dict}")
        elif topic == 'bot_event':
            print(f"Got bot_event: {event_dict}")
        else:
            print(f"Unsupported event_type: {event_dict['event_type']}")

kafka_consumer_task = PythonOperator(
    task_id='kafka_consumer',
    python_callable=listen_kafka,
    dag=dag
)

kafka_consumer_task