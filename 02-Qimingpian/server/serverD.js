const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const func = require('./Qmingpian');

app.use(bodyParser());
app.listen(8000, () => console.log('service start...'));

app.get('/', (req, res) => {
    res.send("welcome!")
});

app.post('/data', (req, res) => {
    let d = req.body;
    let encrypt_data = d.encrypt;
    let result = func.get(encrypt_data);
    res.send(result);
});