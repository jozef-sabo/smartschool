let info;
var relay_info_span = document.getElementById("relay_info");
let graph_div = document.getElementById("graphDIV");
let info_div = document.getElementById("infoDIV");
let interval_id = 0;
let text_graph = 2;

const api_url = "http://192.168.0.105/api/api";

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
    xhttp.open("GET",  api_url + "/get_sensors_aquarium", true);
    xhttp.send();
}

function write() {
    var  content = "";
    content += "<div id='infoFlex'>";
    content += "<p>Čas merania: " + info["time"] + "</p>";
    content += "<p>Teplota vody: " + info["w_temp"] + "°" + info["temp_unit"] + "</p>";
    content += "<p>Teplota vzduchu: " + info["a_temp"] + "°" + info["temp_unit"] + "</p>";
    content += "<p>Vlhkosť vzduchu: " + info["a_hum"] + "%" + "</p>";
    content += "</div>";

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
    xhttp.open("GET", api_url + "/relay/toggle/", true);
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
    xhttp.open("GET", api_url + "/relay/1/toggle/status/", true);
    xhttp.send();
}


function bar() {
    var data;
    $.ajax({
        url: api_url + "/get_sensors_aquarium",
        type: "GET",
        dataType: "json",
        success: function (data) {
            console.log("Success");
            drawBar([data.w_temp, data.a_temp, data.a_hum]);
        },
        error: function () {
            console.log("Error!!!");
        }
    });
    return data;
}

function sk(handleData){
    var data;
        $.ajax({
            url: api_url + "/get_sensors_aquarium",
            type: "GET",
            dataType: "json",
            success: function (data) {
                console.log("Success");
                handleData([data.w_temp, data.a_temp, data.a_hum]);
            },
            error: function () {
                console.log("Error!!!");
            }
        });
        return data;
}

function drawBar(data) {
    var chart1 = new CanvasJS.Chart("humidBar", {
        backgroundColor: "rgba(0,0,0,0)",
        theme: "light2",
        title: {
        text: "Temperature",
        },
        axisY: [{
            title: "C",
            includeZero: true,
        }],
        data: [{
            type: "column",	
            indexLabel: "{y}C",
            dataPoints: [
                {label: "Air", y: data[0], color: "red"},
                {label: "Water", y: data[1], color: "blue"},
        ]
        },
        ]
    });

    var chart2 = new CanvasJS.Chart("tempBar", {
        backgroundColor: "rgba(0,0,0,0)",
        theme: "light2",
        title: {
        text: "Humidity",
        },
        axisY: [{
            title: "%",
            includeZero: true,
        }],
        data: [{
            type: "column",
            indexLabel: "{y}%",
            dataPoints: [
                {label: "Air Humidity", y: data[2], color: "red"},
        ]
        },
        ]
    });


    function updateChart1() {
        sk(function(output) {
            var barColor = "#ADEBD2";
            if(output[0]>40){
                barColor = "#F8A0B0";
            }
            else if(output[0]<35){
                barColor = "#A8E9F0";
            };
            a_temp = {label: "Air", y: output[0], color: barColor};
            barColor = "#ADEBD2";
            if(output[1]>28){
                barColor = "#F8A0B0";
            }
            else if(output[1]<25){
                barColor = "#A8E9F0";
            };
            w_temp = {label: "Water", y: output[1], color: barColor};
            chart1.options.data[0].dataPoints[0] = a_temp;
            chart1.options.data[0].dataPoints[1] = w_temp;
            chart1.render();
        });
    }

    function updateChart2() {
        sk(function(output) {
            a_hum = {label: "Air", y: output[2], color: "#ADEBD2"};
            chart2.options.data[0].dataPoints[0] = a_hum;
            chart2.render();
        });
    }
    updateChart1();
    updateChart2();
    interval_id = setInterval(function() {
        updateChart1();
        updateChart2();
        }, 10000);
}

function on_text_graph_toggle() {
    clearInterval(interval_id)
    if (text_graph === 1) {
        info_div.style.display = "none"
        graph_div.style.display = "initial"
        text_graph = 2
        bar()
        return
    }
    info_div.style.display = "initial"
    graph_div.style.display = "none"
    text_graph = 1
    interval_id = setInterval(function() {get_sensor**REMOVED**()}, 10000);

}

get_sensor**REMOVED**();
statusRelay();
on_text_graph_toggle();
