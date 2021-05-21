var rooms;
let init_load = false;
let darkModeCheckBox;
let darkerRooms;
let lighterRooms;
let emptyRooms;
let chodba;
let h1FontColor;
let buttonDarkMode;
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
    darkModeCheckBox = document.getElementById('darkModeCheckBox');
    darkerRooms = document.getElementsByClassName('darker');
    lighterRooms = document.getElementsByClassName('lighter');
    h1FontColor = document.getElementsByTagName('h1');
    buttonDarkMode = document.getElementsByTagName('button');
    contentTable = document.getElementsByClassName('contentTable');

    if (localStorage.getItem("dark") !== null && localStorage.getItem("dark") === "true") {
        toggle_dark_mode();
        darkModeCheckBox.checked = true;
    }

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
    
    updateTableData();
    let spinnerWrapper = document.querySelector(".spinner-wrapper");
    spinnerWrapper.style.animation = "odlet 0.5s ease-in";
    spinnerWrapper.style.top = "-100%";
    setTimeout(() => {
        spinnerWrapper.parentElement.removeChild(spinnerWrapper);
    }, 500);
}

function toggle_dark_mode() {
    document.body.classList.toggle('dark');

    for (let h1FontColorID = 0; h1FontColorID < h1FontColor.length; h1FontColorID++) { h1FontColor[h1FontColorID].classList.toggle('whiteFont');  }
    for (let buttonDarkModeID = 0; buttonDarkModeID < buttonDarkMode.length; buttonDarkModeID++) { buttonDarkMode[buttonDarkModeID].classList.toggle('buttonDarkMode');}
    for (let contentTableID = 0; contentTableID < contentTable.length; contentTableID++) { contentTable[contentTableID].classList.toggle('tableInDarkMode');}
}

function updateTableData(){
    Object.keys(rooms).forEach((key) => updateTableRow(key));
}

function updateTableRow(room_details) {
    let cell_content = "";

    cell_content += '<td>Trieda '+ room_details +'</td>'

    if ("temperature" in rooms[room_details]) {
        if (rooms[room_details]["temperature"]<18) cell_content += '<td style="color:#79D2E6;">'+rooms[room_details]["temperature"]+'</td>';
        else if (rooms[room_details]["temperature"]<24) cell_content += '<td>'+rooms[room_details]["temperature"]+'</td>';
        else cell_content += '<td style="color:#F67280;">'+rooms[room_details]["temperature"]+'</td>';
    }

    if (rooms[room_details]["humidity"]) {
        if (rooms[room_details]["humidity"]<30) cell_content += '<td style="color:#79D2E6;">'+rooms[room_details]["humidity"]+'</td>';
        else if (rooms[room_details]["humidity"]<50) cell_content += '<td>'+rooms[room_details]["humidity"]+'</td>';
        else cell_content += '<td style="color:#F67280;">'+rooms[room_details]["humidity"]+'</td>';
    }
    if (rooms[room_details]["co2"]) {
        if (rooms[room_details]["co2"]<30) cell_content += '<td style="color:#79D2E6;">'+rooms[room_details]["co2"]+'</td>';
        else if (rooms[room_details]["co2"]<50) cell_content += '<td>'+rooms[room_details]["co2"]+'</td>';
        else cell_content += '<td style="color:#F67280;">'+rooms[room_details]["co2"]+'</td>';


    }
    let element_dom = document.getElementById(room_details);
    if (element_dom) {
        element_dom.innerHTML = cell_content;
    }
}
