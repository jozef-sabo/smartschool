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
    xhttp.open("GET", "http://127.0.0.1:5000/api/get_sensors_aquarium", true);
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
    xhttp.open("GET", "http://127.0.0.1:5000/api/relay/toggle/", true);
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
    xhttp.open("GET", "http://127.0.0.1:5000/api/relay/toggle/status/", true);
    xhttp.send();
}


function bar() {
    var data;
    $.ajax({
        url: "127.0.0.1:5000/api/get_sensors_aquarium",
        type: "GET",
        dataType: "json",
        success: function (data) {
            console.log("Success");
            console.log(data.StatusSNS[0].Temperature);
            // drawBar(data[0][1][1][0]);
            drawBar(data.StatusSNS[0].Temperature);
            // for (var idx = 0; idx < 4; idx++) {
            // drawLine(data[0][idx], idx, data[1], data[2][idx]);
            // }
        },
        error: function () {
            console.log("Error!!!1");
        }
    });
    return data;
};

function drawBar(data) {
    var chart = new CanvasJS.Chart("firstBar", {
        title: {
            text: "Temperature of Each Boiler"
        },
        axisY: {
            title: "Temperature (°C)",
            includeZero: true,
            suffix: " °C"
        },
        data: [{
            type: "column",	
            yValueFormatString: "#,### °C",
            dataPoints: [
                {label: "Temperature", y: data[1]}
            ]
        }]
    });
    
    function updateChart() {
        var barColor, yVal;
        var dps = chart.options.data[0].dataPoints;
        // for (var i = 0; i < dps.length; i++) {

        //     yVal = deltaY + dps[i].y > 0 ? dps[i].y + deltaY : 0;
        //     boilerColor = yVal > 200 ? "#FF2500" : yVal >= 170 ? "#FF6000" : yVal < 170 ? "#6B8E23 " : null;
        //     dps[i] = {label: "Boiler "+(i+1) , y: yVal, color: boilerColor};
        // }
        updated = bar();
        dps[0] = {label: "Temp", y: updated[1]}
        chart.options.data[0].dataPoints = dps; 
        chart.render();
    };
    updateChart();
    
    setInterval(function() {updateChart()}, 500);
}

get_sensor**REMOVED**();
statusRelay();
bar();
