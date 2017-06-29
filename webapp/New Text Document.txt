var express = require('express');
var app = express();
var msg='';
app.use(express.static('public'));
app.get('/index.html', function (req, res) {
   res.sendFile( __dirname + "/" + "index.html" );
})

app.get('/process_get', function (req, res) {
   // Prepare output in JSON format
   response = {
      first_name:req.query.first_name,
      last_name:req.query.last_name
   };
   console.log(response);
   
var myPythonScriptPath = 'test1.py';

var options = {
  mode: 'text',
  pythonOptions: ['-u'],
  args: [req.query.first_name]
};

var message='';
// Use python shell
var PythonShell = require('python-shell');
var pyshell = new PythonShell(myPythonScriptPath,options);

pyshell.on('message', function (message) {
    // received a message sent from the Python script (a simple "print" statement)    
console.log(message);
msg=message;    
});

// end the input stream and allow the process to exit
pyshell.end(function (err) {
    if (err){
        throw err;
    };

    console.log('finished');
});
   res.write(msg);
   res.write(message);
   res.end(JSON.stringify(response));
})

var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port
   console.log("Example app listening at http://%s:%s", host, port)

})