const { sendToKafka } = require('../utils/kafkaProducer');

exports.view = async (req, res) => {
    const location = req.query.location ? req.query.location : "Unknown";
    respJson = {"action": "view", "location": location};
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
    respJson = {"action": "impression", "location": location};
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
    respJson = {"action": "click", "location": location};
    sendToKafka('ad_event', respJson)
        .then(() => {
            console.log("Successfully sent message to Kafka");
        })
        .catch(error => {
            console.error("Failed to send message to Kafka:", error);
        });
    res.json(respJson);
};
