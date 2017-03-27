var express = require('express');
var fs  = require('fs');
var path  = require('path');
var router = express.Router();
var Jimp = require("jimp");

var appRoot = process.cwd();
var imageDest = "/public/modified-keg.png";
var imageSrc = "/public/black-keg.png";
var dataStore = '/tmp/output'

/* GET home page. */
router.get('/', function(req, res, next) {



  if (fs.existsSync(dataStore)) {
    fs.readFile(dataStore, 'utf8', function (err,data) {
      if (err) {
        return console.log(err);
      }
      console.log(data);
      var values = data.split("\n");
      var lastData = parseFloat(values[values.length-2]) / 100;

      recentFreq = values[values.length-2];
      console.log(values);
      console.log(lastData);

      console.log(path.join(appRoot, imageDest));

      Jimp.read(path.join(appRoot, imageSrc), function(err, image) {
        if (err) throw err;
        image.opacity(lastData);// multiply the alpha channel by each pixel by the factor f, 0 - 1
        image.scale(0.25);

        image.write(path.join(appRoot, imageDest), function(err){
          if (err) throw err;
          res.render('index', { title: 'Main' , lastData: lastData});
        });
      });
    });
  }
  else{
    recentFreq = "";
    res.render('index', { title: 'Main' });
  }
});

router.get('/query', function(req, res, next) {
  fs.appendFile("/tmp/output", req.query.freq + "\n", function(err) {
    if(err) {
      return console.log(err);
    }
    console.log("The file was saved!");
  });

  recentFreq = req.query.freq;
  var lastData = parseFloat(recentFreq) / 100;

  res.render('index', { title: 'Query', lastData: lastData});
});

module.exports = router;
