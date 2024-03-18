import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'priority_weight': 10,
}

dag = DAG(
    'kafka_listener_dag',
    default_args=default_args,
    schedule_interval=None,
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
    consumer.subscribe(['ad_event'])

    for message in consumer:
        topic = message.topic
        event = message.value.decode('utf-8')
        print_event(topic, event)

listen_kafka_task = PythonOperator(
    task_id='listen_kafka',
    python_callable=listen_kafka,
    dag=dag
)

listen_kafka_task