import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
import datetime

default_args = {
    'owner': 'airflow',
    'concurrency': 1
}

dag = DAG(
    'kafka_consumer',
    default_args=default_args
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
        print(type(event))

kafka_consumer_task = PythonOperator(
    task_id='kafka_consumer',
    python_callable=listen_kafka,
    dag=dag
)

kafka_consumer_task