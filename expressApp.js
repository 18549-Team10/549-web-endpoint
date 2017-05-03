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
