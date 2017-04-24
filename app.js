const dgram = require('dgram');
const server = dgram.createSocket('udp4');

server.on('error', (err) => {
  console.log(`server error:\n${err.stack}`);
  server.close();
});

server.on('message', (msg, rinfo) => {
  firstTen = msg.slice(0,11).toString('hex');
  var firstData = msg.readUIntLE(0, 4);
  var firstHexData = firstData.toString(16);
  var firstFloat = ((firstData >> 2) & 0xFFF) * 1.4 / 4096;
  console.log(`server got: ${firstData} (${firstHexData}) = ${firstFloat} from ${rinfo.address}:${rinfo.port}`);
});

server.on('listening', () => {
  var address = server.address();
  console.log(`server listening ${address.address}:${address.port}`);
});

server.bind(41234);
// server listening 0.0.0.0:41234
