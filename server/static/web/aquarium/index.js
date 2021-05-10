let info;
var info_div = document.getElementById("info");
var relay_info_span = document.getElementById("relay_info");

function get_sensor**REMOVED**() {
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                info = JSON.parse(this.responseText);
                write();
                return
            }
            console.log("Error");
        }

    };
    xhttp.open("GET", "http://192.168.1.111/api/get_sensors", true);
    xhttp.send();
}

function write() {
    var  content = "";

    const keys = Object.keys(info["StatusSNS"])
    keys.forEach((key, index) => {
        if (isObject(info["StatusSNS"][key])) {
            const keys_2 = Object.keys(info["StatusSNS"][key]);
            keys_2.forEach((key_2, index_2) => {
                content += "<p>" + key_2 + ": " + info["StatusSNS"][key][key_2] + "</p>";
            })
        }
        else {
            content += "<p>" + key + ": " + info["StatusSNS"][key] + "</p>";
        }
    });

    info_div.innerHTML = content;
}

function isObject(objValue) {
  return objValue && typeof objValue === 'object' && objValue.constructor === Object;
}

function toggleRelay() {
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                if (this.responseText !== null && this.responseText !== '') {
                    let relay_info = JSON.parse(this.responseText);
                    relay_info_span.innerText = relay_info["POWER"]
                    }
                    return
            }
            console.log("Error");
        }

    };
    xhttp.open("GET", "http://192.168.1.111/api/relay/toggle/", true);
    xhttp.send();
}

function statusRelay() {
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                if (this.responseText !== null && this.responseText !== '') {
                    let relay_info = JSON.parse(this.responseText);
                    relay_info_span.innerText = relay_info["POWER"]
                }
                return
            }
            console.log("Error");
        }

    };
    xhttp.open("GET", "http://192.168.1.111/api/relay/toggle/status/", true);
    xhttp.send();
}

get_sensor**REMOVED**();
statusRelay();
