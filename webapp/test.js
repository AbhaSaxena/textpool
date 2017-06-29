var express = require('express');
var app = express();
var msg='';
app.use(express.static('public'));
app.get('/example', function (req, res, next) {
  console.log('the response will be sent by the next function ...')
res.send('Hello from A!')
  next()
}, function (req, res) {
  res.write('Hello from B!')
})
var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port
   console.log("Example app listening at http://%s:%s", host, port)

})