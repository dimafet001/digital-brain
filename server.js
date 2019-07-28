const express = require("express");
// var http 	  = require('http').Server(app);
var http	  = require("http");
var https	  = require("https");

var fs 		  = require("fs");
var session   = require("express-session");
const app	  = express();
var h		  = require("okhttp");

// static hosting using express
app.use(express.static("public"));

// Parse URL-encoded bodies (as sent by HTML forms)
// app.use(express.urlencoded());

// Parse JSON bodies (as sent by API clients)
app.use(express.json());

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');  
})

app.get('/get', (req, res) => {
	return getFile();
})




var server = http.createServer(app)
	.listen(8080, '0.0.0.0', () => {
		console.log("running on 8080");
	});


function getFile() {
	var ret = "no";
	https.get('https://api.yuuvis.io/dms/objects/48d1926f-0e0c-456d-885d-3c73622946e6/contents/file', 
		{"Ocp-Apim-Subscription-Key":"2492fd99f01a415c8ce58fe1d92e34bf",
		"Host":"api.yuuvis.io"}	, (res) => { ret = res; })

    return ret;
}