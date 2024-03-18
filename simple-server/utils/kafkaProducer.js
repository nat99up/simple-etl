const { Kafka } = require('kafkajs')

const kafka = new Kafka({
  clientId: 'my-producer-app',
  brokers: ['kafka-0:9092', 'kafka-1:9092'],
})

const producer = kafka.producer()

async function sendToKafka(topic, adEventMessage) {
  await producer.connect();
  // Send the message to the topic
  await producer.send({
    topic: topic,
    messages: [{ value: JSON.stringify(adEventMessage) }],
  });
  await producer.disconnect();
}

exports.sendToKafka = sendToKafka;