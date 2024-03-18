const { sendToKafka } = require('../utils/kafkaProducer');

exports.create = async (req, res) => {
    const duration = isNaN(parseInt(req.query.duration)) ? 30 : parseInt(req.query.duration) // default: 30 sec
    respJson = {"duration": duration};
    sendToKafka('bot_event', respJson)
        .then(() => {
            console.log("Successfully sent message to Kafka");
        })
        .catch(error => {
            console.error("Failed to send message to Kafka:", error);
        });
    res.json(respJson);
};