import asyncio
import aiomysql
import json
from aiokafka import AIOKafkaConsumer

async def create_consumer(topic_name, group_id, bootstrap_servers):
    while True:
        try:
            consumer = AIOKafkaConsumer(
                topic_name, group_id=group_id, bootstrap_servers=bootstrap_servers, enable_auto_commit=True
            )
            await consumer.start()
            print("Succuess created consumer client!")
            break
        except Exception as e:
            await consumer.stop()
            print(f"Error creating consumer: {e}. Retrying...")
            await asyncio.sleep(5)

    return consumer


async def process_ad_event(conn, data):
    cursor = await conn.cursor()
    try:
        await cursor.execute("INSERT INTO ad_events (action, location) VALUES (%s, %s)", (data["action"], data["location"]))
        await conn.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        await cursor.close()


async def consume_messages(consumer):
    try:
        async with aiomysql.connect(host="mysql", port=3306, user="test", password="test", db="simple", loop=asyncio.get_event_loop()) as conn:
            async for msg in consumer:
                # Decode message value and key if necessary
                value = msg.value.decode("utf-8") if isinstance(msg.value, bytes) else msg.value
                key = msg.key.decode("utf-8") if isinstance(msg.key, bytes) else msg.key

                # Process or log the message
                message_string = f"%s:%d:%d: key=%s value=%s" % (
                    msg.topic,
                    msg.partition,
                    msg.offset,
                    key,
                    value,
                )
                print(message_string)
                data = json.loads(value)

                asyncio.create_task(process_ad_event(conn, data))


    finally:
        # Close consumer connection
        await consumer.stop()


async def main():
    topic_name = "ad_event"
    group_id = "py-workers"
    bootstrap_servers = ["kafka-0:9092", "kafka-1:9092"]
    print("Start Worker!")

    # Create Kafka consumer
    await asyncio.sleep(10)
    consumer = await create_consumer(topic_name, group_id, bootstrap_servers)
    await consume_messages(consumer)


if __name__ == "__main__":
    asyncio.run(main())