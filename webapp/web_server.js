
var http = require('http');
var PythonShell = require('python-shell');
http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    
    var shell = new PythonShell('test1.py', { mode: 'text '});
	shell.on('message', function (message) {
  // handle message (a line of text from stdout)
	console.log(message);
    shell.end();
});
res.end('Hello World!');
    
}).listen(8080);