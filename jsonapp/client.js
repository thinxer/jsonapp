var JsonRemote = function(endpoint) {
    this.url = endpoint;
};

JsonRemote.prototype.call = function(method, params, success, error) {
    var req = new XMLHttpRequest();
    req.open("POST", this.url, true);
    req.onreadystatechange = function() {
        if (req.readyState == 4 && req.status == 200) {
            var json = JSON.parse(req.responseText);
            if (json.error && error)
                error(json.error);
            else
                success(json.result);
        }
    };
    req_data = {
        "method": method,
        "params": params
    };
    req.send(JSON.stringify(req_data));
};
