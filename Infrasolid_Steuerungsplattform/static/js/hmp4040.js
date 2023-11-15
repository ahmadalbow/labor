const zyklus = 10000

const currentURL = window.location.href;
const urlParts = new URL(currentURL);

// Extract the IP address
const ipAddress = urlParts.pathname.split("/").pop();

function dataReader() {
    // Construct the URL with query parameters
    const queryParams = new URLSearchParams({ ip: ipAddress });
    const apiUrl = `/api/hmp4040_measure/?${queryParams.toString()}`;

    // Send the GET request
    fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            // You can include other headers if needed, such as authentication tokens
        }
    })
        .then(response => response.json())
        .then(data => {
            for (let i = 1; i < 5; i++) {
                const vp = document.getElementById('v_ch' + i);
                const Ip = document.getElementById('I_ch' + i);
                const Pp = document.getElementById('P_ch' + i);
                vp.textContent = data[i][0].toFixed(3) + "  V";
                Ip.textContent = data[i][1].toFixed(3) + "  A";
                Pp.textContent = data[i][2].toFixed(3) + "  W";
            }
        })
        .catch(error => {
            // Handle any errors that occurred during the fetch
            console.error('Error:', error);
        });

}

const measuerInterval = setInterval(dataReader, 60000);


var data_speichern = document.getElementById("data_speichern");

// Uncheck the checkbox
data_speichern.checked = false;



function startSavingDataRequest(ip) {
    // Prepare the data to be sent in the POST request

    var data = {
        ip: ip

    };

    // Perform the POST request using the Fetch API or another library of your choice
    fetch("/api/start_saving_Data/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
}
function stopSavingDataRequest(ip) {
    // Prepare the data to be sent in the POST request

    var data = {
        ip: ip,

    };

    // Perform the POST request using the Fetch API or another library of your choice
    fetch("/api/stop_saving_Data/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
}
data_speichern.addEventListener("change", function () {
   
    // Create a new Date object representing the current date and time

    // Format the components as "DD-MM-YYYY HH:MM:SS"



    if (this.checked) {
        // Checkbox is checked, start the interval
        startSavingDataRequest(ipAddress)

    } else {
        // Checkbox is unchecked, stop the interval
        stopSavingDataRequest(ipAddress);
    }
});

var popupContainer = document.getElementById("popupContainer");
var closeButton = document.getElementById("closeButton");
if (closeButton != null) {
    closeButton.addEventListener("click", function () {
        popupContainer.style.display = "none";
    });
    for (let i = 1; i < 5; i++) {
        // Get a reference to the input element
        document.getElementById("sollwert_" + i).value = "";
        document.getElementById("auto_korrektur" + i).disabled = true;
        document.getElementById("auto_korrektur" + i).checked = false;
    }
    for (let i = 1; i < 5; i++) {
        // Get a reference to the input element
        var sollwert = document.getElementById("sollwert_" + i);

        // Add an event listener for the "input" event
        sollwert.addEventListener("input", function (event) {
            // This function will be called when the text input changes
            var inputValue = event.target.value;
            if (!(inputValue === "")) {
                document.getElementById("auto_korrektur" + i).disabled = false;
                console.log("Checkbox" + i + " enabled");
            }
            else {
                document.getElementById("auto_korrektur" + i).disabled = true;
                console.log("Checkbox" + i + " disabled");

            }

            // Do something with the changed value

        });

    }
}

var checkboxIds = ["auto_korrektur1", "auto_korrektur2", "auto_korrektur3", "auto_korrektur4"];

// Function to send the POST request
function addChannelReq(ip, ch, sollwert) {
    // Prepare the data to be sent in the POST request
    console.log("ch : " + ch)
    console.log("sollwert : " + sollwert)
    var data = {
        ip: ip,
        ch: ch,
        sollwert: sollwert
    };

    // Perform the POST request using the Fetch API or another library of your choice
    fetch("/api/auto_corrector_add_ch/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })

}
function removeChannelReq(ip, ch) {
    // Prepare the data to be sent in the POST request
    console.log("ch : " + ch)

    var data = {
        ip: ip,
        ch: ch,

    };

    // Perform the POST request using the Fetch API or another library of your choice
    fetch("/api/auto_corrector_remove_ch/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })

}
function isFloat(value) {
    // Use parseFloat to attempt conversion
    const floatValue = parseFloat(value);

    // Check if the result is NaN
    return !isNaN(floatValue);
}
// Loop through the checkbox IDs and add event listeners
var checkbox1 = document.getElementById("auto_korrektur1");
checkbox1.addEventListener("change", function () {
    

    if (this.checked) {
        // Checkbox is checked, start the interval
        console.log("checkbox " + 1 + " is checked")
        if (isFloat(document.getElementById("sollwert_1").value)) {
            addChannelReq(ipAddress, 1, document.getElementById("sollwert_1").value);
        }
        else {
            this.checked = false
        }


        // 20 seconds
    } else {
        // Checkbox is unchecked, stop the interval
        removeChannelReq(ipAddress, 1);
    }
});

var checkbox2 = document.getElementById("auto_korrektur2");

checkbox2.addEventListener("change", function () {

    if (this.checked) {
        // Checkbox is checked, start the interval
        console.log("checkbox " + 2 + " is checked")

        if (isFloat(document.getElementById("sollwert_2").value)) {
            addChannelReq(ipAddress, 2, document.getElementById("sollwert_2").value);
        }
        else {
            this.checked = false
        }
        // 20 seconds
    } else {
        // Checkbox is unchecked, stop the interval
        removeChannelReq(ipAddress, 2);
    }
});

var checkbox3 = document.getElementById("auto_korrektur3");

checkbox3.addEventListener("change", function () {

    if (this.checked) {
        // Checkbox is checked, start the interval
        console.log("checkbox " + 3 + " is checked")

        if (isFloat(document.getElementById("sollwert_3").value)) {
            addChannelReq(ipAddress, 3, document.getElementById("sollwert_3").value);
        }
        else {
            this.checked = false
        }
        // 20 seconds
    } else {
        // Checkbox is unchecked, stop the interval
        removeChannelReq(ipAddress, 3);
    }
});
var checkbox4 = document.getElementById("auto_korrektur4");

checkbox4.addEventListener("change", function () {

    if (this.checked) {
        // Checkbox is checked, start the interval
        console.log("checkbox " + 4 + " is checked")
        if (isFloat(document.getElementById("sollwert_4").value)) {
            addChannelReq(ipAddress, 4, document.getElementById("sollwert_4").value);
        }
        else {
            this.checked = false
        }
        // 20 seconds
    } else {
        // Checkbox is unchecked, stop the interval
        removeChannelReq(ipAddress, 4);
    }
});


function active_channel_req(ip, ch) {
    // Prepare the data to be sent in the POST request

    var data = {
        ip: ip,
        ch: ch,
    };

    // Perform the POST request using the Fetch API or another library of your choice
    fetch("/api/channel_aktivieren/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => {
        })
        .catch(error => {
            console.error("Error:", error);
        });
}
function deactive_channel_req(ip, ch) {
    // Prepare the data to be sent in the POST request

    var data = {
        ip: ip,
        ch: ch,
    };

    // Perform the POST request using the Fetch API or another library of your choice
    fetch("/api/channel_deaktivieren/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => {
        })
        .catch(error => {
            console.error("Error:", error);
        });
}
auto_corrector_status
let hiddenChannelsStatus = document.getElementById('hidden_channels_status').textContent
console.log(hiddenChannelsStatus)
const hiddenChannelsStatusArray = JSON.parse(hiddenChannelsStatus);

for (let i = 0; i < 4; i++) {

    if (hiddenChannelsStatusArray[i] === 1) {
        document.getElementById('ch' + (i + 1)).checked = true
    } else {
        // Checkbox is unchecked, stop the interval
        document.getElementById('ch' + (i + 1)).checked = false
    }

}

let autoCorrectorStatus = document.getElementById('auto_corrector_status').textContent
const autoCorrectorStatusArray = JSON.parse(autoCorrectorStatus);
for (let i = 0; i < 4; i++) {

    document.getElementById('auto_korrektur' + (1 + i)).checked = false

}
for (let i = 0; i < autoCorrectorStatusArray.length; i++) {

    document.getElementById('auto_korrektur' + autoCorrectorStatusArray[i]).checked = true

}
let is_saving_running = document.getElementById('is_saving_running').textContent
if (is_saving_running === "True") {
    document.getElementById('data_speichern').checked = true
}
else {
    document.getElementById('data_speichern').checked = false
}
for (let i = 1; i < 5; i++) {
    document.getElementById('ch' + i).addEventListener("change", function () {
        console.log("clicked")
        if (this.checked) {
            // Checkbox is checked, start the interval
            active_channel_req(ipAddress, i); // 20 seconds
        } else {
            // Checkbox is unchecked, stop the interval
            deactive_channel_req(ipAddress, i);
        }
    });
}
function enable_out_req(ip, ch) {
    // Prepare the data to be sent in the POST request

    var data = {
        ip: ip,
        ch: ch,
    };

    // Perform the POST request using the Fetch API or another library of your choice
    fetch("/api/out_aktivieren/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => {
        })
        .catch(error => {
            console.error("Error:", error);
        });
}
function disable_out_req(ip, ch) {
    // Prepare the data to be sent in the POST request

    var data = {
        ip: ip,
        ch: ch,
    };

    // Perform the POST request using the Fetch API or another library of your choice
    fetch("/api/out_deaktivieren/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => {
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

document.getElementById("out").addEventListener("change", function () {
    console.log("clicked")
    if (this.checked) {
        // Checkbox is checked, start the interval
        enable_out_req(ipAddress); // 20 seconds
    } else {
        // Checkbox is unchecked, stop the interval
        disable_out_req(ipAddress);
    }
});
