const dgram = require('dgram');
const server = dgram.createSocket('udp4');
const fs  = require('fs');
const path  = require('path');
const PythonShell = require('python-shell');
const spawn = require('child_process').spawn;
const os = require("os");

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
const lastFrequency = 31000;
const firstChunk = 0;
const firstFrequency = 10000;
var iterationsSeen = 0;
const totalIterations = 1;
const fillLevels = ["ERROR", "EMPTY", "QUARTER", "HALF", "THREE_Q", "FULL", "UNKNOWN"];

var options = {
  mode: 'text',
  scriptPath: appRoot + '/scripts/',
  args: ["1", "1"] //keg, debug
};

function processPythonRun (fillLevel, err, results) {
  if(os.platform() == 'win32') return;
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  //console.log('results: %j', results);
  results.forEach(line => console.log(line));
  fs.readdir(graphDirectory + path.sep + fillLevel, function(err, items) {
    items = items.filter((f) => fs.statSync(graphDirectory + path.sep + fillLevel + path.sep + f).isFile());
    if (items.length > 0){
      //spawn("eog", [graphDirectory + path.sep + fillLevel + path.sep + items[0]]);
    }
  });
}

//PythonShell.run('rawToFill.py', options, (err,results) => processPythonRun("", err, results));

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
    if(chunk == lastChunk && frequency == lastFrequency && fillLevel == "UNKNOWN"){
      iterationsSeen+=1;
      console.log("Last chunk %d of 8", iterationsSeen);
      if(iterationsSeen == totalIterations){
        iterationsSeen = 0;
        PythonShell.run('rawToFill.py', options,
                        (err,results) => processPythonRun(fillLevel, err, results));
      }
    }
  });
});

server.on('listening', () => {
  var address = server.address();
  console.log(`server listening ${address.address}:${address.port}`);
});

server.bind(41234);
// server listening 0.0.0.0:41234

//Run express app
require('./expressApp.js');
