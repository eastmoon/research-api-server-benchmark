// njs script
function addValue(r) {
    r.return(200, `{'result': '${parseInt(r.variables["v1"]) + parseInt(r.variables["v2"])}'}`);
}

function strReplace(r) {
    let res = r.variables["org"].replaceAll(r.variables["pattern"], r.variables["replacement"]);
    r.return(200, `{'result': '${res}'}`);
}

export default { addValue, strReplace };
