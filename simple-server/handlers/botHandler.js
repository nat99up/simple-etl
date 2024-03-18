const { sendToKafka } = require('../utils/kafkaProducer');

exports.create = async (req, res) => {
    const duration = req.query.duration ? req.query.duration : 30; // default: 30 sec
    respJson = {"event_type": "bot_event", "action": "view", "location": location};
    sendToKafka('bot_event', respJson)
        .then(() => {
            console.log("Successfully sent message to Kafka");
        })
        .catch(error => {
            console.error("Failed to send message to Kafka:", error);
        });
    res.json(respJson);
};