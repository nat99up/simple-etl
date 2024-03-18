const express = require('express');
const app = express();
const adRoutes = require('./routes/adRoutes');
const botRoutes = require('./routes/botRoutes')

app.get('/', (req, res) => {
    res.json({"action": "Hello"});
});

app.use('/ad', adRoutes);
app.use('/bot', botRoutes)

app.listen(8888, () => {
  console.log('Server started on port 8888');
});