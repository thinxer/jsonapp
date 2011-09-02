var JsonRemote = function(endpoint) {
    this.url = endpoint;
};

JsonRemote.prototype.call = function(method, params, callback) {
    var req = new XMLHttpRequest();
    req.open("POST", this.url, true);
    req.onreadystatechange = function() {
        if (req.readyState == 4) {
            if (req.status == 200) {
                var json = JSON.parse(req.responseText);
                callback(json.error, json.result);
            } else {
                callback({ "code": req.status, "err": req.statusText }, req);
            }
        }
    };
    req_data = {
        "method": method,
        "params": params
    };
    req.send(JSON.stringify(req_data));
};
