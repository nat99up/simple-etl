import asyncio
import aiohttp
import random
import time
import airflow
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
    locations = ["US", "UK", "DE", "FR", "JP", "CN"]

    # 開始計時
    start_time = time.time()

    while time.time() - start_time < duration:
        # 隨機生成 action 和 location
        action = random.choice(actions)
        location = random.choice(locations)

        data = {
            "action": action,
            "location": location,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url.format(action=action, location=location), headers=headers) as response:
                if response.status == 200:
                    print(f"Sent ad event: {action} - {location}")
                else:
                    print(f"Failed to send ad event: {action} - {location} - Status: {response.status}")
        await asyncio.sleep(random.uniform(0.5, 1))


def run_async(duration):
   loop = asyncio.get_event_loop()
   result = loop.run_until_complete(post_ad_events_to_simple_server(duration))
   return result

async_task = PythonOperator(
    task_id='bot_handler',
    python_callable=run_async,
    op_kwargs={'duration': 10},  # 傳遞給非同步函數的參數
    dag=dag,
)
async_task
