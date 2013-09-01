var fs = require("fs");

var inputFile = process.argv[2]; //'./tagged-split-06-rodrigo-fuenzalida';

var data = '';

fs.readFileSync(inputFile).toString().split('\n').forEach(function (line) { 
	data = '';
    var parse = line.toString().split("\t");
    var category = parse.shift();
    var query = parse.shift();

    data += category + '\t' + query + '\n';

    fs.appendFileSync('new_'+inputFile, data);
});

