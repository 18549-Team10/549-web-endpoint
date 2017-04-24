const dgram = require('dgram');
const server = dgram.createSocket('udp4');
const fs  = require('fs');
const path  = require('path');

const appRoot = process.cwd();
const dataDirectory = appRoot + path.sep + 'data';
const dataFilename = 'output';
const dataPath = dataDirectory + path.sep + dataFilename;
const dataBytes = 4;
const dataOutputBase = 16;

function convertData(data){
  return ((data >> 2) && 0xFFF);
}

server.on('error', (err) => {
  console.log(`server error:\n${err.stack}`);
  server.close();
});

server.on('message', (msg, rinfo) => {
  firstTen = msg.slice(0,11).toString('hex');
  var firstData = (msg.readUIntLE(0, dataBytes));
  var firstHexData = firstData.toString(dataOutputBase);
  var firstFloat = convertData(firstData) * 1.4 / 4096;
  console.log(`server got: ${firstData} (${firstHexData}) = ${firstFloat} from ${rinfo.address}:${rinfo.port}`);
  var data = []
  for(var i = 0; i < msg.length; i+=dataBytes){
    data.push(msg.readUIntLE(i, dataBytes),
                  "\n");
  }

  if (!fs.existsSync(dataDirectory)){
        fs.mkdirSync(dataDirectory);
  }

  fs.appendFile(dataPath, data.join(""), function(err) {
    if(err) {
      return console.log(err);
    }
    console.log("The file was saved!");
  });
});

server.on('listening', () => {
  var address = server.address();
  console.log(`server listening ${address.address}:${address.port}`);
});

server.bind(41234);
// server listening 0.0.0.0:41234
