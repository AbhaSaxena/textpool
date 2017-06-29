var express = require('express');
var app = express();
var msg='';
var myPythonScriptPath = 'file_sent.py';

var message='';
// Use python shell
var PythonShell = require('python-shell');

app.use(express.static('public'));
app.get('/index2.html', function (req, res) {
   res.sendFile( __dirname + "/" + "index2.html" );
})

app.get('/process_get', function (req, res) {
   // Prepare output in JSON format
   response = {
      file_name:req.query.file_name
   };
   console.log(response);

var options = {
  mode: 'text',
  pythonOptions: ['-u'],
  args: [req.query.file_name]
};

PythonShell.run(myPythonScriptPath , options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
res.sendFile( __dirname + "/" + "index.html" );
});

 //res.end("fin."); 
})

var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port
   console.log("Example app listening at http://%s:%s", host, port)

})