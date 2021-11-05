var express = require('express');
var app = express();
var cors = require('cors')

const path = require('path');

app.use(cors())
app.use('/', express.static(path.join(__dirname, 'public')))

var port = 3000;
app.listen(port, function () {
    console.log(`Server running on http://localhost:${port}`);
    console.log(`Data at http://localhost:${port}/pageviews?parameter1=10&parameter2=AAA`);
})

app.get('/pageviews', function (req, res) {
    var spawn = require('child_process').spawn;
    var process = spawn('python', ['./pageviews_data.py',
        // video id and user id
        req.query.parameter1,
        req.query.parameter2]
    );
    process.stdout.on('data', function (data) {
        res.send(data);
    });
});

app.get('/watchtime', function (req, res) {
    var spawn = require('child_process').spawn;
    var process = spawn('python', ['./watchtime_data.py',
        req.query.parameter1,
        req.query.parameter2]
    );
    process.stdout.on('data', function (data) {
        res.send(data);
    });
});
