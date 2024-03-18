const { Kafka } = require('kafkajs')

const kafka = new Kafka({
  clientId: 'my-producer-app',
  brokers: ['kafka-0:9092', 'kafka-1:9092'],
})

let producer; // Declare producer outside the function for persistence

async function connectProducer() {
  if (!producer) {
    producer = kafka.producer();
    await producer.connect();
  }
}

async function sendToKafka(topic, adEventMessage) {
  await connectProducer(); // Ensure connection before sending

  // Send the message to the topic
  await producer.send({
    topic: topic,
    messages: [{ value: JSON.stringify(adEventMessage) }],
  });
}

exports.sendToKafka = sendToKafka;