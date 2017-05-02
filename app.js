const dgram = require('dgram');
const server = dgram.createSocket('udp4');
const fs  = require('fs');
const path  = require('path');
const PythonShell = require('python-shell');
const spawn = require('child_process').spawn;

const appRoot = process.cwd();
const dataDirectory = appRoot + path.sep + 'data';
const graphDirectory = appRoot + path.sep + 'graphs';
const dataFilename = 'output';
const dataBytes = 4;
const dataOutputBase = 16;

const headerSize = 12;
const frequencyIndex = 0;
const chunkIndex = 1;
const fillIndex = 2;
const lastChunk = 3;
const lastFrequency = 6000;
const fillLevels = ["ERROR", "EMPTY", "QUARTER", "HALF", "THREE_Q", "FULL"];

var options = {
  mode: 'text',
  scriptPath: appRoot + '/scripts/',
  args: [""]
};

function processPythonRun (fillLevel, err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
  fs.readdir(graphDirectory + path.sep + fillLevel, function(err, items) {
    items = items.filter((f) => fs.statSync(graphDirectory + path.sep + fillLevel + path.sep + f).isFile());
    if (items.length > 0){
      spawn("eog", [graphDirectory + path.sep + fillLevel + path.sep + items[0]]);
    }
  });
}


PythonShell.run('visualizer.py', options, (err,results) => processPythonRun("", err, results));

function convertData(data){
  return ((data >> 2) && 0xFFF);
}

server.on('error', (err) => {
  console.log(`server error:\n${err.stack}`);
  server.close();
});

server.on('message', (msg, rinfo) => {
  var firstData = (msg.readUIntLE(headerSize, dataBytes));
  var firstHexData = firstData.toString(dataOutputBase);
  var firstFloat = convertData(firstData) * 1.4 / 4096;
  var frequency = (msg.readUIntLE(frequencyIndex, dataBytes));
  var chunk = (msg.readUIntLE(chunkIndex * dataBytes, dataBytes));
  var fillLevel = fillLevels[(msg.readUIntLE(fillIndex * dataBytes, dataBytes))];


  console.log(`server got: ${firstHexData} = ${firstFloat} from ${rinfo.address}:${rinfo.port} for ${frequency}:${chunk}`);
  var data = []
  for(var i = headerSize; i < msg.length; i+=dataBytes){
    data.push(msg.readUIntLE(i, dataBytes),
                  "\n");
  }

  var dataTarget = dataDirectory + path.sep + fillLevel;
  //Full path to data
  var dataPath = dataTarget + path.sep + dataFilename;
  options.args[0] = fillLevel;

  if (!fs.existsSync(dataDirectory)){
    fs.mkdirSync(dataDirectory);
  }
  if (!fs.existsSync(dataTarget)){
    fs.mkdirSync(dataTarget);
  }

  fs.appendFile(dataPath+("0" + frequency).slice(-5), data.join(""), function(err) {
    if(err) {
      return console.log(err);
    }
    console.log("The file was saved!");
    // if(chunk == lastChunk && frequency == lastFrequency){
    //   PythonShell.run('visualizer.py', options,
    //                   (err,results) => processPythonRun(fillLevel, err, results));
    // }
  });
});

server.on('listening', () => {
  var address = server.address();
  console.log(`server listening ${address.address}:${address.port}`);
});

server.bind(41234);
// server listening 0.0.0.0:41234

// Import Express module for Express framework
const express = require('express');

// Import handlebars for HTML templating
var exphbs = require('express-handlebars');

// Create Express app
var app = express();

app.engine('handlebars',
	exphbs({
		defaultLayout: 'main',
		helpers: 'helpers'
	})
);
app.set('view engine', 'handlebars');

app.use('/', express.static(__dirname + '/public/'));

app.get('/', function(req, res) {
	//res.send('Hello World!');
	res.render('index');
});

app.get('/containers', function(req, res) {
	res.render('containers');
});

// Declaring which port # the app should be listening on
var port = process.env.PORT || 3000;

// App is listening on the declared port #
app.listen(port, function() {
	console.log("Listening on port " + port + "!");
});
