import time
from kafka import KafkaConsumer, KafkaAdminClient


def create_topic(admin_client, topic_name, partitions=1, replication_factor=1):
    """
    Creates a Kafka topic if it doesn't already exist.

    Args:
        admin_client (KafkaAdminClient): The Kafka admin client.
        topic_name (str): The name of the topic to create.
        partitions (int, optional): The number of partitions for the topic. Defaults to 1.
        replication_factor (int, optional): The replication factor for the topic. Defaults to 1.
    """

    try:
        # Check if topic exists
        topics = admin_client.list_topics().topics
        if topic_name not in topics:
            # Create topic if it doesn't exist
            new_topics = [KafkaAdminClient.NewTopic(topic_name, partitions, replication_factor)]
            admin_client.create_topics(new_topics=new_topics)
            print(f"Created topic: {topic_name}")
    except Exception as e:
        print(f"Error creating topic {topic_name}: {e}")


def main():
    topic_name = "ad_event"
    group_id = "py-workers"
    bootstrap_servers = ["kafka-0:9092", "kafka-1:9092"]
    print("Start Worker!")

    # Create Kafka admin client
    while True:
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
            print("Succuess created admin client!")
            break
        except Exception as e:
            print(f"Error creating admin: {e}")
            time.sleep(3)  # Retry after 3 seconds

    # Create topic if it doesn't exist
    create_topic(admin_client, topic_name)


    # Create Kafka consumer
    while True:
        try:
            consumer = KafkaConsumer(
                topic_name, group_id=group_id, bootstrap_servers=bootstrap_servers
            )
            print("Succuess created consumer client!")
            break  # Exit the loop if consumer creation succeeds
        except Exception as e:
            print(f"Error creating consumer: {e}")
            time.sleep(3)  # Retry after 3 seconds

    
    for message in consumer:
        # Decode message value and key if necessary
        value = message.value.decode("utf-8") if isinstance(message.value, bytes) else message.value
        key = message.key.decode("utf-8") if isinstance(message.key, bytes) else message.key

        # Process or log the message
        message_string = f"%s:%d:%d: key=%s value=%s" % (
            message.topic,
            message.partition,
            message.offset,
            key,
            value,
        )
        print(message_string)
            


if __name__ == "__main__":
    main()
