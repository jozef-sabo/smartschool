/* 18 - 68 */
var rooms;
let init_load = false;
// Okno s detailmi
//const open = document.getElementById('open');
let popUpWindowID;
let close;
const api_url = "http://127.0.0.1:5000/api";

//TEMPORARY DATA FOR TESTING
/*room_details_001 = { "id":"room_001", "temperature": 10.0, "humidity": 37.0, "co2": 40 }
room_details_002 = { "id":"room_002", "temperature": 23.0, "humidity": 40.0, "co2": 40 }
room_details_003 = { "id":"room_003", "temperature": 22.0, "humidity": 39.0, "co2": 39}
room_details_004 = { "id":"room_004", "temperature": 21.0, "humidity": 60.0, "co2": 40 }
room_details_005 = { "id":"room_005", "temperature": 22.0, "humidity": 38.0, "co2": 38}
room_details_006 = { "id":"room_006", "temperature": 20.0, "humidity": 37.0, "co2": 40 }
room_details_007 = { "id":"room_007", "temperature": 23.0, "humidity": 40.0, "co2": 40 }
room_details_008 = { "id":"room_008", "temperature": 22.0, "humidity": 39.0, "co2": 39}
room_details_009 = { "id":"room_009", "temperature": 21.0, "humidity": 37.0, "co2": 40 }
room_details_010 = { "id":"room_010", "temperature": 22.0, "humidity": 38.0, "co2": 38}
room_details_011 = { "id":"room_011", "temperature": 22.0, "humidity": 39.0, "co2": 39}
room_details_012 = { "id":"room_012", "temperature": 21.0, "humidity": 37.0, "co2": 40 }
room_details_013 = { "id":"room_013", "temperature": 22.0, "humidity": 38.0, "co2": 38}
room_details_014 = { "id":"room_014", "temperature": 20.0, "humidity": 37.0, "co2": 40 }
room_details_015 = { "id":"room_015", "temperature": 23.0, "humidity": 40.0, "co2": 40 }
room_details_016 = { "id":"room_016", "temperature": 22.0, "humidity": 39.0, "co2": 39}
room_details_017 = { "id":"room_017", "temperature": 21.0, "humidity": 37.0, "co2": 40 }
room_details_018 = { "id":"room_018", "temperature": 22.0, "humidity": 38.0, "co2": 38}*/
const temporary_rooms = {
    "units": {"temperature": "°C", "humidity": "%", "co2": "ppm"},
    /*"room_001": {"temperature": 10.0, "humidity": 37.0, "co2": 40},
    "room_002": {"temperature": 23.0, "humidity": 40.0, "co2": 40},*/
    "room_003": {"temperature": 22.0, "humidity": 39.0, "co2": 39},
    "room_004": {"temperature": 21.0, "humidity": 60.0, "co2": 40},
    "room_005": {"temperature": 22.0, "humidity": 38.0, "co2": 38},
    "room_006": {"temperature": 20.0, "humidity": 37.0, "co2": 40},
    "room_007": {"temperature": 23.0, "humidity": 40.0, "co2": 40},
    "room_008": {"temperature": 22.0, "humidity": 39.0, "co2": 39},
    "room_009": {"temperature": 21.0, "humidity": 37.0, "co2": 40},
    "room_010": {"temperature": 22.0, "humidity": 38.0, "co2": 38},
    "room_011": {"temperature": 22.0, "humidity": 39.0, "co2": 39},
    "room_012": {"temperature": 21.0, "humidity": 37.0, "co2": 40},
    "room_013": {"temperature": 22.0, "humidity": 38.0, "co2": 38},
    "room_014": {"temperature": 20.0, "humidity": 37.0, "co2": 40},
    "room_015": {"temperature": 23.0, "humidity": 40.0, "co2": 40},
    "room_016": {"temperature": 22.0, "humidity": 39.0, "co2": 39},
    "room_017": {"temperature": 21.0, "humidity": 37.0, "co2": 40},
    "room_018": {"temperature": 22.0, "humidity": 38.0, "co2": 38}
}
/*const temporary_rooms = [room_details_003, room_details_004, room_details_005, room_details_006, room_details_007, room_details_008,
    room_details_009, room_details_010, room_details_011, room_details_012, room_details_013, room_details_014,
    room_details_015, room_details_016, room_details_017, room_details_018]*/

var xhttp;
xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState === 4) {
        if (this.status === 200) {
            console.log("Success");
            rooms = Object.assign({}, temporary_rooms, JSON.parse(this.responseText));
            if (!init_load) {
                init_load = true;
                return
            }
            init();
            return;
        }
        console.log("Error", this.status);
        rooms = temporary_rooms;
        if (!init_load) {
            init_load = true;
            return
        }
        init();
    }

};
xhttp.open("GET", api_url + '/get_sensors', true);
xhttp.timeout = 2000;
xhttp.send();


document.addEventListener("DOMContentLoaded", function(){
    if (!init_load) {
            init_load = true;
            return
        }
    init();
});

function init() {
    popUpWindowID = document.getElementById('popUpWindowID');
    close = document.getElementById('close');
    close.addEventListener('click',()=> {
        popUpWindowID.classList.remove('show');
        bodyID.classList.remove('noscroll');
    })
    Object.keys(rooms).forEach(key => update_room_details(key, rooms[key]))
    let spinnerWrapper = document.querySelector(".spinner-wrapper");
    spinnerWrapper.style.animation = "odlet 0.5s ease-in";
    spinnerWrapper.style.top = "-100%";
    document.getElementById("obsah").style.display = "initial";
    setTimeout(() => {
        spinnerWrapper.parentElement.removeChild(spinnerWrapper);
        }, 500);

}


/* 390 - 869 */
// console.log("My script starting here.");


    //update_all_room_details();});

function update_all_room_details(){
    $.ajax({
        url: api_url + '/get_sensors',
        type: "GET",
        dataType: "json",
        success: function (data) {
            console.log("Success");
            rooms = Object.assign({}, temporary_rooms, JSON.parse(this.responseText));
            rooms.forEach((key, value) => update_room_details(key, value));
        },
        error: function (xhr) {
            console.log("Error", xhr.status);
        }
    });
}


/*
function update_all_room_details(){

for (i=0; i<rooms.length; i++){
update_room_details(rooms[i]);
}
}
*/

function update_room_details(id, details) {
    if (!document.getElementById(id)) return;
    let cell_content = "";

    if ("temperature" in details) {
        cell_content += '<p><span class="fas fa-thermometer-half fa-xs"></span> '+details["temperature"] + rooms["units"]["temperature"] +'</p>';
    }
    if ("humidity" in details) {
        cell_content += '<p><span class="fas fa-tint fa-xs"></span> '+details["humidity"]+ rooms["units"]["humidity"] +'</p>';
    }
    if ("co2" in details) {
        cell_content += '<p>CO<sub>2</sub> '+details["co2"] + rooms["units"]["co2"] +'</p>';
    }
    document.getElementById(id).innerHTML = cell_content;

    if ((details["temperature"]<18) || (details["temperature"]>24) || (details["humidity"]<30) || (details["humidity"]>50) || (details["co2"]<30) || (details["co2"]>50)) {
        document.getElementById(id).className = "room orangeRoom";
    }
}

function openDetails(room_details) {
    let cell_content = "";
    let cell_content2 = "";

    if ("temperature" in room_details) {
        if (room_details["temperature"]<18){
            cell_content += '<p class="blue detailsWindow"><span class="fas fa-thermometer-half fa-xs"></span> '+room_details["temperature"]+'°C</p>';
        } else if (room_details["temperature"]<24) {
            cell_content += '<p class="detailsWindow"><span class="fas fa-thermometer-half fa-xs"></span> '+room_details["temperature"]+'°C</p>';
        } else {
            cell_content += '<p class="red detailsWindow"><span class="fas fa-thermometer-half fa-xs"></span> '+room_details["temperature"]+'°C</p>';
        }
    }

    if ("humidity" in room_details) {
        if (room_details["humidity"]<30) {
            cell_content += '<p class="blue detailsWindow"><span class="fas fa-tint fa-xs"></span> '+room_details["humidity"]+'%</p>';
        } else if (room_details["humidity"]<50) {
            cell_content += '<p class="detailsWindow"><span class="fas fa-tint fa-xs"></span> '+room_details["humidity"]+'%</p>';
        } else {
            cell_content += '<p class="red detailsWindow"><span class="fas fa-tint fa-xs"></span> '+room_details["humidity"]+'%</p>';
        }
    }

    if ("co2" in room_details) {
        if (room_details["co2"]<30) {
            cell_content += '<p class="blue detailsWindow">CO<sub>2</sub> '+room_details["co2"]+'ppm</p>';
        } else if (room_details["co2"]<50) {
            cell_content += '<p class="detailsWindow">CO<sub>2</sub> '+room_details["co2"]+'ppm</p>';
        } else {
            cell_content += '<p class="red detailsWindow">CO<sub>2</sub> '+room_details["co2"]+'ppm</p>';
        }
    }

    cell_content2 += '<br><br><button class="leftButton" onclick="candle()">Show Candle</button>';
    cell_content2 += '<button class="rightButton" onclick="line()">Show Line</button><br><br>';
    cell_content2 += '<div><button class="leftButton" onclick="dateSub()"><span class="fas fa-chevron-left"></span></button><button class="rightButton" onclick="dateAdd()"><span class="fas fa-chevron-right"></span></button></div><br><br></div>' ;
    cell_content2 += '<div class="graph"><div id="chartTemp" style="height: 300px; width: 100%;"></div></div><br><br>'
    cell_content2 += '<div class="graph"><div id="chartHumid" style="height: 300px; width: 100%;"></div></div><br><br>'
    cell_content2 += '<div class="graph"><div id="chartDP" style="height: 300px; width: 100%;"></div></div><br><br>'
    cell_content2 += '<div class="graph"><div id="chartA0" style="height: 300px; width: 100%;"></div></div><br><br>'

    document.getElementById("detailsInPopUp").innerHTML = cell_content;
    document.getElementById("detailsInPopUpPt2").innerHTML = cell_content2;
    popUpWindowID.classList.add('show');
    bodyID.classList.add('noscroll');
    candle();
}






//open.addEventListener('click',()=>{
//    popUpWindowID.classList.add('show');
//})




/* DATA FOR TESTING

room_details_001 = { "id":"room_001", "temperature": 5.0, "humidity": 5.0, "co2": 5 }
room_details_002 = { "id":"room_002", "temperature": 22.0, "humidity": 40.0, "co2": 40 }
room_details_003 = { "id":"room_003", "temperature": 100.0, "humidity": 100.0, "co2": 100 }

rooms = [room_details_001, room_details_002, room_details_003]
*/
var type;
function candle() {
    type = 0;
    console.log(type);
    var data;

    $.ajax({
        url: api_url + '/Candle',
        type: "GET",
        dataType: "json",
        success: function (data) {
            console.log("Success");
            for (var idx = 0; idx < 4; idx++) {
            drawCandle(data[0][idx], idx, data[1]);
            }
        },
        error: function () {
            console.log("Errorr!");
        }
    });
    return data;
}

function line() {
    type = 1;
    console.log(type);
    var data;
    $.ajax({
        url: api_url + '/Line',
        type: "GET",
        dataType: "json",
        success: function (data) {
            console.log("Success");
            for (var idx = 0; idx < 4; idx++) {
            drawLine(data[0][idx], idx, data[1][idx], data[2]);
            }
        },
        error: function () {
            console.log("Error!");
        }
    });
    return data;
}

function dateSub() {
    if(type == 0) {
        $.ajax({
            url: api_url + '/CandleSub',
            type: "GET",
            dataType: "json",
            success: function (data) {
                console.log("Success");
                for (var idx = 0; idx < 4; idx++) {
                drawCandle(data[0][idx], idx, data[1]);
                }
            },
            error: function () {
                console.log("Errorr!");
            }
        })
    }
    if(type == 1) {
        $.ajax({
            url: api_url + '/LineSub',
            type: "GET",
            dataType: "json",
            success: function (data) {
                console.log("Success");
                for (var idx = 0; idx < 4; idx++) {
                drawLine(data[0][idx], idx, data[1][idx], data[2]);
                }
            },
            error: function () {
                console.log("Error!");
            }
        })
    }
}

function dateAdd() {
    if(type == 0) {
        $.ajax({
            url: api_url + '/CandleAdd',
            type: "GET",
            dataType: "json",
            success: function (data) {
                console.log("Success");
                for (var idx = 0; idx < 4; idx++) {
                drawCandle(data[0][idx], idx, data[1]);
                }
            },
            error: function () {
                console.log("Errorr!");
            }
        })
    }
    if(type == 1) {
        $.ajax({
            url: api_url + '/LineAdd',
            type: "GET",
            dataType: "json",
            success: function (data) {
                console.log("Success");
                for (var idx = 0; idx < 4; idx++) {
                drawLine(data[0][idx], idx, data[1][idx], data[2]);
                }
            },
            error: function () {
                console.log("Error!");
            }
        })
    }
}

function drawCandle(data, idx, date) {
    date = new Date(date);
    yyyy = date.getFullYear();
    mm = date.getMonth()+1;
    dd = date.getDate();
    subtitleDate = dd + '/' + mm + '/' + yyyy;
    // console.log(createDatapoints(y));
    sensor = selectSensorType(idx);
    var chart = new CanvasJS.Chart(sensor[0], {
        animationEnabled: true,
        backgroundColor: "rgba(255, 255, 255, 0)",
        theme: "light2",
        dataPointWidth: 10,
        title: {
            text: sensor[1],
            fontColor: 'gray',
        },
        subtitles: [{
            text: subtitleDate,
            // text: "Hourly Candles",
            fontColor: 'gray',
        }],
        axisY: {
            title: sensor[2],
            minimum: 0,
            maximum: sensor[3],
            lineColor:'gray',
            labelFontSize: 10,
            labelFontColor: 'gray',
            gridThickness:0,
        },
        axisX: {
            title: "Hour",
            lineColor:'gray',
            labelFontSize: 10,
            labelFontColor: 'gray',
            interval: 1,
            minimum: 0,
            maximum: 24,
        },
        toolTip: {
            shared: false,
            contentFormatter: function ( e ) {
                var content = "";
                for (var i = 0; i < e.entries.length; i++) {
                    y = e.entries[i].dataPoint.y;
                    x = e.entries[i].dataPoint.x;
                    if(Array.isArray(y)) {
                        content += "Hour: " + x + "<br /><strong>Values:</strong><br />Open: " + y[0] + ", Close: " + y[3] + "<br />High: " + y[1] + ", Low: " + y[2];
                    } else {
                        content += "Hour: "+ x + "<br /><strong>Value:</strong><br />" + y;
                    }
                }
            return content
            }
        },
        data: [
            {
                type: "spline",
                dataPoints: createOHLCpoints(data, 3), //0 - open, 1 - high, 2 - low, 3 - close
                markerType: 'none',
                lineColor: '#ABC1C4',
                lineThickness: 1,
            },
            {
                type: "candlestick",
                xValueType: "int",
                dataPoints: createDatapoints(data),
                //fallingColor: '#79D2E6',
                fallingColor: '#DA4467',
                //risingColor: '#F67280',
                risingColor: '#69B5A6',
                color:'rgb(200, 200, 200)',
            },
        ]
    });

    function createOHLCpoints(data, x) {
        var dataPoints = [];
        for (var i = 0; i < data.length; i++) {
            dataPoints.push( {
                x: data[i][0],
                y: data[i][1][x]
            })
        }
        return dataPoints
    }
    changeBorderColor(chart);
    chart.render();
}

function drawLine(data, idx, avg, date) {
    date = new Date(date);
    yyyy = date.getFullYear();
    mm = date.getMonth()+1;
    dd = date.getDate();
    subtitleDate = dd + '/' + mm + '/' + yyyy;

    sensor = selectSensorType(idx);
    var chart = new CanvasJS.Chart(sensor[0], {
        animationEnabled: true,
        backgroundColor: "rgba(255, 255, 255, 0)",
        title:{
            text: sensor[1],
        },
        subtitles: [{
            text: subtitleDate,
            // text: "Hourly Candles",
            fontColor: 'gray',
        }],
        axisY: {
            stripLines: [{
                value: avg,
                label: "Average",
                lineColor:'white',
                color: 'rgb(235, 146, 0)',
                gridThickness: 0,
                lineThickness: 5,
            }],
            title: sensor[2],
            maximum: sensor[3],
            minimum: 0,
            labelFontSize: 10,
            labelFontColor: 'gray',
            gridThickness:0,
            fontColor: 'rgb(235, 146, 0)',
            lineThickness:0,
        },
        axisX: {
            title: "Hour",
            lineColor:'gray',
            labelFontSize: 10,
            labelFontColor: 'gray',
            gridThickness:0,
            interval: 1,
            minimum: 0,
            maximum: 24,
        },

        data: [{
            type: "line",
            dataPoints: createDatapoints(data),
            color: '#ABC1C4',
            markerType: 'none',
            lineThickness:4,
        }]
    });
    chart.render();
}


function selectSensorType(idx) {
    if (idx == 0) {
        ch = "chartTemp";
        title = 'Temperature';
        unit = '°C';
        max = 35;
    }
    if (idx == 1) {
        ch = "chartHumid";
        title = "Humidity";
        unit = '%';
        max = 90;
    }
    if (idx == 2) {
        ch = "chartDP";
        title = "Dew Point";
        unit = '-';
        max = 35;
    }
    if (idx == 3) {
        ch = "chartA0";
        title = "A0";
        unit = "ppm";
        max = 5;
    }
    return [ch, title, unit, max]
}

// returns in format [{x1: value1, y1: value1, value2,...},{x2:... , y2:... },...]
function createDatapoints(data) {
    var dataPoints = [];
    for (var i = 0; i < data.length; i++) {
        dataPoints.push( {
            x: data[i][0],
            y: data[i][1]
        })
    }
    return dataPoints
}

function changeBorderColor(chart) {
    var dataSeries;
    for( var i = 0; i < chart.options.data.length; i++) {
        dataSeries = chart.options.data[i];
        for(var j = 0; j < dataSeries.dataPoints.length; j++) {
            dataSeries.dataPoints[j].color = (dataSeries.dataPoints[j].y[0] <= dataSeries.dataPoints[j].y[3]) ? (dataSeries.risingColor ? dataSeries.risingColor : dataSeries.color) : (dataSeries.fallingColor ? dataSeries.fallingColor : dataSeries.color);
        }
    }
}
