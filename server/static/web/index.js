let rooms;
let init_load = false;
let selected_class;
// Okno s detailmi
//const open = document.getElementById('open');
let popUpWindowID;
let close;
let bodyID;
let detailsInPopup;
let detailsInPopup2;
let darkModeCheckBox;
let darkerRooms;
let lighterRooms;
let emptyRooms;
let chodba;
let h1FontColor;
let popUpInDarkMode;
let buttonDarkMode;
let classNamePopUp;
let contentTable;

const api_url = "http://10.0.7.59:5000/api";

//TEMPORARY DATA FOR TESTING
const temporary_rooms = {
    "units": {"temperature": "°C", "humidity": "%", "co2": "ppm"},
    /*"room_001": {"temperature": 10.0, "humidity": 37.0, "co2": 40},
    "room_002": {"temperature": 23.0, "humidity": 40.0, "co2": 40},*/
    "room_003": {"temperature": 22.0, "humidity": 39.0, "co2": 39},
    "room_004": {"temperature": 21.0, "humidity": 60.0, "co2": 40},
    "room_005": {"temperature": 22.0, "humidity": 38.0, "co2": 38},
    /*"room_006": {"temperature": 20.0, "humidity": 37.0, "co2": 40},*/
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

let xhttp;
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
            setTimeout(() => init(), 100);
            return;
        }
        console.log("Error", this.status);
        rooms = temporary_rooms;
        if (!init_load) {
            init_load = true;
            return
        }
        setTimeout(() => init(), 100);
    }

};
xhttp.open("GET", api_url + '/get_sensors', true);
xhttp.timeout = 2000;
xhttp.send();


document.addEventListener("DOMContentLoaded", function() {
    if (!init_load) {
        init_load = true;
        return
    }
    setTimeout(() => init(), 100);
});

function init() {
    bodyID = document.getElementById("bodyID");
    popUpWindowID = document.getElementById('popUpWindowID');
    close = document.getElementById('close');
    detailsInPopup = document.getElementById("detailsInPopUp");
    detailsInPopup2 = document.getElementById("detailsInPopUpPt2");
    classNamePopUp = document.getElementById("classNamePopUp");

    darkModeCheckBox = document.getElementById('darkModeCheckBox');
    darkerRooms = document.getElementsByClassName('darker');
    lighterRooms = document.getElementsByClassName('lighter');
    emptyRooms = document.getElementsByClassName('room');
    chodba = document.getElementsByClassName('chodba');
    h1FontColor = document.getElementsByTagName('h1');
    popUpInDarkMode = document.getElementsByClassName("popUp");
    buttonDarkMode = document.getElementsByTagName('button');
    contentTable = document.getElementsByClassName('contentTable');
    resetDate();

    if (localStorage.getItem("dark") !== null && localStorage.getItem("dark") === "true") {
        toggle_dark_mode();
        darkModeCheckBox.checked = true;
    }

    close.addEventListener('click',()=> {
        popUpWindowID.classList.remove('show');
        bodyID.classList.remove('noscroll');
    });

    darkModeCheckBox.addEventListener('change', () => {
        if (localStorage.getItem("dark") !== null) {
            if (localStorage.getItem("dark") === "true") localStorage.setItem("dark", "false");
            else localStorage.setItem("dark", "true");
        } else {
            if (emptyRooms[0].classList.contains("roomInDarkMode")) localStorage.setItem("dark", "false");
            else localStorage.setItem("dark", "true");
        }
        toggle_dark_mode();
    });
    

    Object.keys(rooms).forEach(key => update_room_details(key, rooms[key]))
    let spinnerWrapper = document.querySelector(".spinner-wrapper");
    spinnerWrapper.style.animation = "odlet 0.5s ease-in";
    spinnerWrapper.style.top = "-100%";
    updateTableData();
    document.getElementById("obsah").style.display = "initial";
    setTimeout(() => {
        spinnerWrapper.parentElement.removeChild(spinnerWrapper);
    }, 500);
}

function toggle_dark_mode() {
    document.body.classList.toggle('dark');
    for (let emptyRoomsID = 0; emptyRoomsID < emptyRooms.length; emptyRoomsID++) { emptyRooms[emptyRoomsID].classList.toggle('roomInDarkMode');}
    for (let darkerID = 0; darkerID < darkerRooms.length; darkerID++) { darkerRooms[darkerID].classList.toggle('darkerInDarkMode'); }
    for (let lighterID = 0; lighterID < lighterRooms.length; lighterID++) { lighterRooms[lighterID].classList.toggle('lighterInDarkMode'); }
    for (let chodbaID = 0; chodbaID < chodba.length; chodbaID++) { chodba[chodbaID].classList.toggle('chodbaInDarkMode'); }
    for (let h1FontColorID = 0; h1FontColorID < h1FontColor.length; h1FontColorID++) { h1FontColor[h1FontColorID].classList.toggle('whiteFont');  }
    for (let popUpInDarkModeID = 0; popUpInDarkModeID < popUpInDarkMode.length; popUpInDarkModeID++) { popUpInDarkMode[popUpInDarkModeID].classList.toggle('popUpInDarkMode'); }
    for (let buttonDarkModeID = 0; buttonDarkModeID < buttonDarkMode.length; buttonDarkModeID++) { buttonDarkMode[buttonDarkModeID].classList.toggle('buttonDarkMode');}
    for (let contentTableID = 0; contentTableID < contentTable.length; contentTableID++) { contentTable[contentTableID].classList.toggle('tableInDarkMode');}
}

function update_all_room_details(){
    $.ajax({
        url: api_url + '/get_sensors',
        type: "GET",
        dataType: "json",
        success: function (data) {
            console.log("Success");
            rooms = Object.assign({}, temporary_rooms, data);
            rooms.forEach((key, value) => update_room_details(key, value));
        },
        error: function (xhr) {
            console.log("Error", xhr.status);
        }
    });
}

function update_room_details(id, details) {
    let id_element = document.getElementById(id);
    if (!id_element) return;
    let cell_content = "";

    if ("temperature" in details) {cell_content += '<p><span class="fas fa-thermometer-half fa-xs"></span> '+ details["temperature"] + rooms["units"]["temperature"] +'</p>';}
    if ("humidity" in details) {cell_content += '<p><span class="fas fa-tint fa-xs"></span> '+details["humidity"] + rooms["units"]["humidity"] +'</p>';}
    if ("co2" in details) {cell_content += '<p>CO<sub>2</sub> '+ details["co2"] + rooms["units"]["co2"] +'</p>';}
    id_element.innerHTML = cell_content;

    if (
        (details["temperature"] < 18) || (details["temperature"] > 24) ||
        (details["humidity"] < 30) || (details["humidity"] > 50) ||
        (details["co2"] < 30) || (details["co2"] > 50)
    ) id_element.className = "room orangeRoom";
}

function updateTableData(){
    for (i=0; i<rooms.length; i++){
    updateTableRow(rooms[i]);}
    }

function updateTableRow(room_details) {
    cell_content = "";
    room_number=i+1;

    cell_content += '<td>Trieda '+room_number+'</td>'

    if ("temperature" in room_details)
    {
    
        if (room_details["temperature"]<18)
            {
                cell_content += '<td style="color:#79D2E6;">'+room_details["temperature"]+'</td>';
            }
            else if (room_details["temperature"]<24)
                {
                    cell_content += '<td>'+room_details["temperature"]+'</td>';
                }
                else
                    {
                        cell_content += '<td style="color:#F67280;">'+room_details["temperature"]+'</td>';
                    } 

    }



    if (room_details["humidity"])
    {
    
        if (room_details["humidity"]<30)
            {
                cell_content += '<td style="color:#79D2E6;">'+room_details["humidity"]+'</td>';
            }
            else if (room_details["humidity"]<50)
                {
                    cell_content += '<td>'+room_details["humidity"]+'</td>';
                }
                else
                    {
                        cell_content += '<td style="color:#F67280;">'+room_details["humidity"]+'</td>';
                    } 

    }
    if (room_details["co2"])
    {

        if (room_details["co2"]<30)
            {
                cell_content += '<td style="color:#79D2E6;">'+room_details["co2"]+'</td>';
            }
            else if (room_details["co2"]<50)
                {
                    cell_content += '<td>'+room_details["co2"]+'</td>';
                }
                else
                    {
                        cell_content += '<td style="color:#F67280;">'+room_details["co2"]+'</td>';
                    } 


    }
    document.getElementById(room_details["id"]).innerHTML = cell_content;
    }

function openDetails(id) {
    let cell_content = "";
    let cell_content2 = "";
    let color;

    if ("temperature" in rooms[id]) {
        color = "";
        if (rooms[id]["temperature"] > 24) color = "red";
        if (rooms[id]["temperature"] < 18) color = "blue";
        cell_content += '<p class="detailsWindow ' + color + '"><span class="fas fa-thermometer-half fa-xs"></span> ' + rooms[id]["temperature"] + rooms["units"]["temperature"] +'</p>';
    }

    if ("humidity" in rooms[id]) {
        color = "";
        if (rooms[id]["humidity"] > 50) color = "red";
        if (rooms[id]["humidity"] < 30) color = "blue";
        cell_content += '<p class="detailsWindow ' + color + '"><span class="fas fa-tint fa-xs"></span> ' + rooms[id]["humidity"] + rooms["units"]["humidity"] + '</p>';
    }

    if ("co2" in rooms[id]) {
        color = "";
        if (rooms[id]["co2"] > 50) color = "red";
        if (rooms[id]["co2"] < 30) color = "blue";
        cell_content += '<p class="detailsWindow ' + color + '">CO<sub>2</sub> ' + rooms[id]["co2"]+ rooms["units"]["co2"] + '</p>';
    }

    //cell_content2 += '<br><br><button class="leftButton" onclick="candle(selected_class)">Show Candle</button>';
    //cell_content2 += '<button class="rightButton" onclick="line(selected_class)">Show Line</button><br><br>';
    //cell_content2 += '<div><button class="leftButton" onclick="dateSub(selected_class)"><span class="fas fa-chevron-left"></span></button><button class="rightButton" onclick="dateAdd(selected_class)"><span class="fas fa-chevron-right"></span></button></div><br><br></div>' ;
    cell_content2 += '<div class="graph" style="background-color:rgba(0,0,0,0)"><div id="chartTemp" style="height: 300px; width: 100%;"></div></div><br><br>'
    cell_content2 += '<div class="graph" style="background-color:rgba(0,0,0,0)"><div id="chartHumid" style="height: 300px; width: 100%;"></div></div><br><br>'
    cell_content2 += '<div class="graph" style="background-color:rgba(0,0,0,0)"><div id="chartDP" style="height: 300px; width: 100%;"></div></div><br><br>'
    cell_content2 += '<div class="graph" style="background-color:rgba(0,0,0,0)"><div id="chartA0" style="height: 300px; width: 100%;"></div></div><br><br>'

    classNamePopUp.innerText = "Detaily o triede " + id;
    detailsInPopup.innerHTML = cell_content;
    detailsInPopup2.innerHTML = cell_content2;
    popUpWindowID.classList.add('show');
    bodyID.classList.add('noscroll');
    resetDate();
    selected_class = id;
    candle(selected_class);
}

//open.addEventListener('click',()=>{
//    popUpWindowID.classList.add('show');
//})

var type;
function resetDate() {
    $.ajax({
        url: api_url + '/ResetDate',
        type: "GET",
    });
}
function candle(selected_class) {
    type = 0;
    var data;
    console.log(selected_class);
    $.ajax({
        url: api_url + '/Candle/' + selected_class + "/",
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

function line(selected_class) {
    type = 1;
    console.log(selected_class);
    var data;
    $.ajax({
        url: api_url + '/Line/' + selected_class + "/",
        type: "GET",
        dataType: "json",
        success: function (data) {
            console.log("Success");
            for (var idx = 0; idx < 4; idx++) {
            drawLine(data[0][idx], idx, data[1], data[2][idx]);
            }
        },
        error: function () {
            console.log("Error!");
        }
    });
    return data;
}

function dateSub(selected_class) {
    if(type == 0) {
        $.ajax({
            url: api_url + '/CandleSub/' + selected_class + "/",
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
            url: api_url + '/LineSub/' + selected_class + "/",
            type: "GET",
            dataType: "json",
            success: function (data) {
                console.log("Success");
                for (var idx = 0; idx < 4; idx++) {
                drawLine(data[0][idx], idx, data[1], data[2][idx]);
                }
            },
            error: function () {
                console.log("Error!");
            }
        })
    }
}

function dateAdd(selected_class) {
    if(type == 0) {
        $.ajax({
            url: api_url + '/CandleAdd/' + selected_class + "/",
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
            url: api_url + '/LineAdd/' + selected_class + "/",
            type: "GET",
            dataType: "json",
            success: function (data) {
                console.log("Success");
                for (var idx = 0; idx < 4; idx++) {
                drawLine(data[0][idx], idx,  data[1], data[2][idx]);
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
    mm = (date.getMonth())+1;
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

function drawLine(data, idx, myDate, sigma) {
    date = new Date(myDate);
    yyyy = date.getFullYear();
    mm = (date.getMonth())+1;
    dd = date.getDate();
    subtitleDate = dd + '/' + mm + '/' + yyyy;

    sensor = selectSensorType(idx);
    var chart = new CanvasJS.Chart(sensor[0], {
        animationEnabled: true,
        backgroundColor: "rgba(255, 255, 255, 0)",
        theme: "light2",
        title:{
            text: sensor[1],
            fontColor: 'gray',
        },
        subtitles: [{
            text: subtitleDate,
            fontColor: 'gray',
        }],
        axisY: {
            stripLines: [
            {
                startValue: sigma[0],
                endValue: sigma[1],
                label: "+-3σ",
                labelFormatter: function(e){
                    if (sigma[0] == 0 && sigma[1] == 0){
                        return " "
                    }
                    else{
                        return e.stripLine.label
                    }
                },
                labelBackgroundColor: "rgba(0,0,0,0)",
                labelFontColor: "#FFB485",
                color:"rgba(255,180,133,0.2)",
            }
            ],
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
        toolTip: {
            content: "<br/><strong>Hour: </strong>{x}<br /><strong>Value: </strong>{y}" 
        },
        data: [{
            type: "spline",
            dataPoints: createDatapoints(data),
            color: '#ABC1C4',
            markerType: 'none',
            lineThickness:2.5,
        },
    ]
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
        unit = '°C';
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
        dataPoints.push(
            {x: data[i][0], 
            y: data[i][1]})
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
