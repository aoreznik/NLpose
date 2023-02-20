const fs = require('fs');
const config = require('./config.json');

var files = [];

var read_data_dir = function() {
    let local_files = fs.readdirSync(config.data_dir);
    let results = require(config.results_file);
    local_files.forEach( (file) => {
        let result = results['results'].find( (el) => {
            return el.id == file;
        });
        if ((file.match(/.+\.jpg/))&&(result != undefined)) {
            files.push({
                "id": file,
                "path": config.data_dir + "/" + file,
                "result": result["result"].split(',').map(el => el.trim())
            });

        }
    });
};

var get_random_file = function() {
    var id = Math.round(Math.random() * (files.length - 1));

    let data = fs.readFileSync(files[id]['path']);
    data = new Buffer(data, 'binary').toString('base64');
    return {
        'id': files[id]['id'],
        'data': data,
        'result': files[id]['result']
    }
};



read_data_dir();

module.exports.get = get_random_file;