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

app.get('/statistics', function(req, res) {
	res.render('statistics');
});

app.get('/notifications', function(req, res) {
	res.render('notifications');
});

app.get('/settings', function(req, res) {
	res.render('settings');
});

app.get('/about-us', function(req, res) {
	res.render('about-us');
});

app.get('/sign-out', function(req, res) {
	res.render('sign-out');
});

// Declaring which port # the app should be listening on
var port = process.env.PORT || 3000;

// App is listening on the declared port #
app.listen(port, function() {
	console.log("Listening on port " + port + "!");
});
