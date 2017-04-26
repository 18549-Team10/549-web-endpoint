const dgram = require('dgram');
const server = dgram.createSocket('udp4');
const fs  = require('fs');
const path  = require('path');
const PythonShell = require('python-shell');

const appRoot = process.cwd();
const dataDirectory = appRoot + path.sep + 'data';
const dataFilename = 'output';
const dataPath = dataDirectory + path.sep + dataFilename;
const dataBytes = 4;
const dataOutputBase = 16;

const headerSize = 8;
const frequencyIndex = 0;
const chunkIndex = 1;
const lastChunk = 3;
const lastFrequency = 6000;

var options = {
  mode: 'text',
  scriptPath: appRoot + '/scripts/',
  args: [dataDirectory]
};

PythonShell.run('entry.py', options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
});

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

  console.log(`server got: ${firstHexData} = ${firstFloat} from ${rinfo.address}:${rinfo.port} for ${frequency}:${chunk}`);
  var data = []
  for(var i = headerSize; i < msg.length; i+=dataBytes){
    data.push(msg.readUIntLE(i, dataBytes),
                  "\n");
  }

  if (!fs.existsSync(dataDirectory)){
        fs.mkdirSync(dataDirectory);
  }

  fs.appendFile(dataPath+("0" + frequency).slice(-5), data.join(""), function(err) {
    if(err) {
      return console.log(err);
    }
    console.log("The file was saved!");
    if(chunk == lastChunk && frequency == lastFrequency){
      PythonShell.run('entry.py', options, function (err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        console.log('results: %j', results);

      });
    }
  });
});

server.on('listening', () => {
  var address = server.address();
  console.log(`server listening ${address.address}:${address.port}`);
});

server.bind(41234);
// server listening 0.0.0.0:41234
