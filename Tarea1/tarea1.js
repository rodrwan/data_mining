var fs = require("fs");
var Table = require("cli-table");

var inputFile = process.argv[2]; //'./tagged-split-06-rodrigo-fuenzalida';

var table = new Table({
        head: ['INF', 'NAV', 'RES', 'Total', 'Entropy'],
        colWidths: [20, 20, 20, 20, 20]
    }); 

var cuentaNAV = 0,
    cuentaINF = 0,
    cuentaRES = 0;


fs.readFileSync(inputFile).toString().split('\n').forEach(function (line) { 
	data = '';
    var parse = line.toString().split("\t");
    var glosa = parse.shift();
    if (glosa.indexOf('NAV') > -1){
        cuentaNAV++;
    }
    if (glosa.indexOf('INF') > -1){
        cuentaINF++;
    }
    if (glosa.indexOf('RES') > -1){
        cuentaRES++;
    }
});

function log2(val) {
  return Math.log(val) / Math.log(2);
}
var total = cuentaNAV + cuentaRES + cuentaINF,
    PrNAV = cuentaNAV/total,
    PrRES = cuentaRES/total,
    PrINF = cuentaINF/total;
var res = -( PrNAV*log2(PrNAV) + PrRES*log2(PrRES) + PrINF*log2(PrINF) );
table.push( [cuentaINF, cuentaNAV, cuentaRES, total, res.toFixed(3)] );
console.log(table.toString());

