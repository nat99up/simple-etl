const express = require('express');
const app = express();
const adRoutes = require('./routes/adRoutes');

app.get('/', (req, res) => {
    res.json({"action": "Hello"});
});

app.use('/ad', adRoutes);

app.listen(8888, () => {
  console.log('Server started on port 8888');
});