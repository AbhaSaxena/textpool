var express = require('express');
var app = express();
var msg='';
var myPythonScriptPath = 'file_sent.py';
var myPythonScriptPath2 = 'tfidf_blob.py';
var myPythonScriptPath3 = 'tfidf_blob1.py';
var message='';
global.filename;
// Use python shell
var PythonShell = require('python-shell');

app.use(express.static('public'));
app.get('/index2.html', function (req, res) {
   res.sendFile( __dirname + "/" + "index2.html" );
})
app.get('/index.html', function (req, res) {
   res.sendFile( __dirname + "/" + "index.html" );
})
app.get('/loaded.html', function (req, res) {
   res.sendFile( __dirname + "/" + "loaded.html" );
})
app.get('/loading2.html', function (req, res) {
   res.sendFile( __dirname + "/" + "loading2.html" );
})
app.get('/process_get', function (req, res) {
   // Prepare output in JSON format
   response = {
      file_name:req.query.file_name
   };
global.filename=req.query.file_name;
   console.log(response);
res.sendFile( __dirname + "/" + "loading.html" );

var options = {
  mode: 'text',
  pythonOptions: ['-u'],
  args: [req.query.file_name]
};
PythonShell.run(myPythonScriptPath2 , options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
console.log('file name is : '+global.filename);

});

 //res.end("fin."); 
})
app.get('/loading2', function (req, res) {
   // Prepare output in JSON format
res.sendFile( __dirname + "/" + "loading2.html" );

var options = {
  mode: 'text',
  pythonOptions: ['-u'],
  args: [global.filename]
};

PythonShell.run(myPythonScriptPath , options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);

});

 //res.end("fin."); 
})


app.get('/corpus_type',  function (req, res) {
   // Prepare output in JSON format
response = {
      corpus:req.query.corpustype
   };
console.log(response);
res.sendFile( __dirname + "/" + "loading2.html" );
var options = {
  mode: 'text',
  pythonOptions: ['-u'],
  args: [global.filename]
};

/*PythonShell.run(myPythonScriptPath , options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
//return res.redirect('/index.html');
});*/
if(req.query.corpustype!='yes')
{
var options1 = {
  mode: 'text',
  pythonOptions: ['-u'],
  args: [global.filename,req.query.corpustype]
};
PythonShell.run(myPythonScriptPath3 , options1, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
console.log('file name is : '+global.filename);

});

}
 //res.end("fin."); 
})


var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port
   console.log("Example app listening at http://%s:%s", host, port)

})