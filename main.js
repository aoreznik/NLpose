const { spawn } = require('child_process');
const CONFIG = require('./config.json');
const data = require("./data.js");
const request = require("request");

var error_tests = 0;

var test_request = function () {

    let file = data.get();
    console.log(file['id']);
    console.log(file['data'].length);
    let options = {
        //url: "http://82.112.188.38:11052/processImage",
        url: "http://localhost:11052/processImage",
        method: "POST",
        body: JSON.stringify({id: 0, img: file['data']})
    };

    return new Promise( (resolve, reject) => {
        request.post(options, (err, res, body) => {
            if (err) {
                console.log(err);
            }
            else {
                body = JSON.parse(body);
                //console.log(file['result']);
                //console.log(body['result']);
                let missing = 0;
                let missing_arr = [];
                let over = 0;
                let over_arr = []
                file['result'].forEach( (t) => {
                    if (body['result'].find( el => t == el) == undefined) missing_arr.push(t);
                });
                body['result'].forEach( (t) => {
                    if (file['result'].find( el => t == el) == undefined) over_arr.push(t);
                });
                console.log(JSON.stringify(body['result']));
                console.log(JSON.stringify(file['result']));
                console.log("missing: ", missing_arr);
                console.log("over: ", over_arr);

                if (missing_arr.length + over_arr.length == 0) {
                    resolve(true);
                } else {
                    resolve(false);
                }
            }
        });
    });
};

var process;

var start_server = function() {
    process = spawn('python', ["../combined-models.txt"]) ;

    process.on('close', () => console.log('server stopped'));
    process.stdout.setEncoding('utf8');
    process.stdout.on('data', function(data) {
        //Here is where the output goes

        console.log('stdout: ' + data);

        data=data.toString();
        scriptOutput+=data;
    });
};

var kill_server = function() {
    process.kill();
};

//test_request();
start_server();

var test_timeout = setInterval( () => {
    console.log("Error_tests: ", error_tests);
    test_request().then( (res) => {
        console.log(res);
        if (!res) error_tests++;
    });

    if (error_tests > 3) {
        kill_server();
        start_server();
        error_tests = 0;
    }
}, 1000 * 60 * 1);