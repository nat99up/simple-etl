import asyncio
import aiohttp
import random
import time
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
}

dag = DAG(
    'bot_handler',
    default_args=default_args,
    schedule_interval=None
)


async def post_ad_events_to_simple_server(duration):
    url = "http://simple-server:8888/ad/{action}?location={location}"
    headers = {"Content-Type": "application/json"}
    actions = ["view", "click", "impression"]
    locations = ["US", "UK", "DE", "FR", "JP", "CN", "IN", "AU", "BR", "MX"]

    # 開始計時
    start_time = time.time()

    while time.time() - start_time < duration:
        # 隨機生成 action 和 location
        action = random.choice(actions)
        location = random.choice(locations)

        async with aiohttp.ClientSession() as session:
            async with session.post(url.format(action=action, location=location), headers=headers) as response:
                if response.status == 200:
                    print(f"Sent ad event: {action} - {location}")
                else:
                    print(f"Failed to send ad event: {action} - {location} - Status: {response.status}")
        await asyncio.sleep(random.uniform(0.2, 1))


def run_async(duration):
    print(f"Get param duration = {duration}")
    try:
        duration = int(duration)
    except ValueError:
        duration = 30
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(post_ad_events_to_simple_server(duration))
    return result

async_task = PythonOperator(
    task_id='bot_handler',
    python_callable=run_async,
    op_kwargs={'duration': "{{ dag_run.conf['duration'] }}"},
    dag=dag,
)
async_task
