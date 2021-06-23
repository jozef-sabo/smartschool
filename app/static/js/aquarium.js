let info;
let graph_div = document.getElementById("graphDIV");
let info_div = document.getElementById("infoDIV");
let air_button = document.getElementById("leftButton");
let bulb_button = document.getElementById("rightButton");
let interval_id = 0;
let text_graph = 2;

// const api_url = "http://10.0.7.174:5000/api";
// const api_url = "http://10.0.7.59:5000/api";
const api_url = "http://localhost:5000/aquarium/api";


function get_sensors_data() {
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

function getCookie(name) {
    var cookieArr = document.cookie.split(";");
    for(let i = 0; i < cookieArr.length; i++) {
        let cookiePair = cookieArr[i].split("=");
        if(name === cookiePair[0].trim()) {
            return decodeURIComponent(cookiePair[1]);
        }
    }
    return null;
}

function logged_in() {
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                let is_logged_in = getCookie("logged_in");
                if (is_logged_in) {
                    if (is_logged_in === "true") {
                        setTimeout(() => {
                            statusRelay(1);
                            statusRelay(2);
                            setInterval(function() {statusRelay(1);statusRelay(2);}, 20000);
                        })
                    }

                }
                return
            }
            console.log("Error");
        }

    };
    xhttp.open("GET", api_url + "/../../api/logged_in", true);
    xhttp.send();
}

function toggleRelay(id) {
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                if (this.responseText !== null && this.responseText !== '') {
                    let relay_info = JSON.parse(this.responseText);
                    set_buttons_colors(relay_info, id);
                }
                return
            }
            console.log("Error");
        }

    };
    xhttp.open("GET", api_url + "/relay/" + id + "/toggle/", true);
    xhttp.send();
}

function pustKrmitko(pocetOtacok) {
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                if (this.responseText !== null && this.responseText !== '') {
                    console.log("Done");
                }
                return
            }
            console.log("Error");
        }

    };
    xhttp.open("GET", api_url + "/feed/" + pocetOtacok, true);
    xhttp.send();
}

function statusRelay(id) {
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                if (this.responseText !== null && this.responseText !== '') {
                    let relay_info = JSON.parse(this.responseText);
                    set_buttons_colors(relay_info, id)
                }
                return

            }
            console.log("Error");
        }

    };
    xhttp.open("GET", api_url + "/relay/" + id + "/toggle/status/", true);
    xhttp.send();
}

function set_buttons_colors(relay_info, id) {
    if (id == 1) {
        if (relay_info["POWER"] === "OFF") {
            air_button.classList.add("indicatorOFF")
            air_button.classList.remove("indicatorON")
            return;
        }

        if (relay_info["POWER"] === "ON") {
            air_button.classList.add("indicatorON")
            air_button.classList.remove("indicatorOFF")
            return;
        }
        return;
    }

    if (id == 2) {
        if (relay_info["POWER"] === "OFF") {
            bulb_button.classList.add("indicatorOFF")
            bulb_button.classList.remove("indicatorON")
            return;
        }

        if (relay_info["POWER"] === "ON") {
            bulb_button.classList.add("indicatorON")
            bulb_button.classList.remove("indicatorOFF")
        }
    }
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
            title: " °C",
            includeZero: true,
            maximum: 60,
        }],
        data: [{
            type: "column",	
            indexLabel: "{y}C",
            dataPoints: [
                {label: "Air", y: data[1], color: "red"},
                {label: "Water", y: data[0], color: "blue"},
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
            title: " %",
            maximum: 100,
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
            if(output[1]>40){
                barColor = "#F8A0B0";
            }
            else if(output[1]<35){
                barColor = "#A8E9F0";
            };
            a_temp = {label: "Air", y: output[1], color: barColor};
            barColor = "#ADEBD2";
            if(output[0]>28){
                barColor = "#F8A0B0";
            }
            else if(output[0]<25){
                barColor = "#A8E9F0";
            };
            w_temp = {label: "Water", y: output[0], color: barColor};
            chart1.options.data[0].dataPoints[1] = a_temp;
            chart1.options.data[0].dataPoints[0] = w_temp;
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
    interval_id = setInterval(function() {get_sensors_data()}, 10000);

}

get_sensors_data();
logged_in();
on_text_graph_toggle();
