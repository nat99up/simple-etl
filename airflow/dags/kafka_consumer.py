from airflow import DAG
from airflow.operators.python import PythonOperator
import datetime
import json
import psycopg2

def insert_event_data(event_data):
  connection = psycopg2.connect(dbname="airflow", user="airflow", password="airflow", host="postgres", port=5432)
  cursor = connection.cursor()

  insert_statement = """
    INSERT INTO ad_events (action, location)
    VALUES (%s, %s)
  """
  cursor.execute(insert_statement, (event_data["action"], event_data["location"]))
  connection.commit()
  cursor.close()
  connection.close()

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

        try:
            event_data = json.loads(event)
            if topic == 'ad_event':
                print(f"Got ad_event: {event_data}")
                insert_event_data(event_data)
                print("Insertion Successful!")
            elif topic == 'bot_event':
                print(f"Got bot_event: {event_data}")
            else:
                print(f"Unsupported topic: {topic}")
        except:
            print("Something wrong")


kafka_consumer_task = PythonOperator(
    task_id='kafka_consumer',
    python_callable=listen_kafka,
    dag=dag
)

kafka_consumer_task