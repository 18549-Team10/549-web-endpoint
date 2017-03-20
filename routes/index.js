var express = require('express');
var fs  = require('fs');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  fs.readFile('/tmp/output', 'utf8', function (err,data) {
    if (err) {
      return console.log(err);
    }
    console.log(data);
    recentFreq = data;

    res.render('index', { title: 'Main' });
  });
});

router.get('/query', function(req, res, next) {
  fs.appendFile("/tmp/output", req.query.freq + "\n", function(err) {
    if(err) {
      return console.log(err);
    }
    console.log("The file was saved!");
  });

  recentFreq = req.query.freq;

  res.render('index', { title: 'Query' });
});

module.exports = router;
