const { Kafka } = require('kafkajs')

const kafka = new Kafka({
  clientId: 'my-producer-app',
  brokers: ['kafka-0:9092', 'kafka-1:9092'],
})

const producer = kafka.producer()

async function sendToKafka(topic, adEventMessage)
{
    // Connect to Kafka
    await producer.connect();

    // Send the message to the topic
    await producer.send({
        topic: topic,
        messages: [{ value: JSON.stringify(adEventMessage) }],
    });

    // Disconnect from Kafka
    await producer.disconnect();
}

exports.view = async (req, res) => {
    const location = req.query.location ? req.query.location : "Unknown";
    respJson = {"action": "View", "location": location};
    sendToKafka('ad_event', respJson)
        .then(() => {
            console.log("Successfully sent message to Kafka");
        })
        .catch(error => {
            console.error("Failed to send message to Kafka:", error);
        });
    res.json(respJson);
};

exports.impression = async (req, res) => {
    const location = req.query.location ? req.query.location : "Unknown";
    respJson = {"action": "Impression", "location": location};
    sendToKafka('ad_event', respJson)
        .then(() => {
            console.log("Successfully sent message to Kafka");
        })
        .catch(error => {
            console.error("Failed to send message to Kafka:", error);
        });
    res.json(respJson);
};

exports.click = async (req, res) => {
    const location = req.query.location ? req.query.location : "Unknown";
    respJson = {"action": "Click", "location": location};
    sendToKafka('ad_event', respJson)
        .then(() => {
            console.log("Successfully sent message to Kafka");
        })
        .catch(error => {
            console.error("Failed to send message to Kafka:", error);
        });
    res.json(respJson);
};
