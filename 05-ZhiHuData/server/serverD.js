const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const func = require('./zh.js');

//解析 body
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));
app.listen(8888, () => console.log('service start...'));

app.get('/', (req, res) => {
    res.send("welcome!")
});

app.post('/data', (req, res) => {
    let d = req.body;
    let encrypt_data = d.param;
    let result = func.get_encrypt(encrypt_data);
    res.send(result);
});