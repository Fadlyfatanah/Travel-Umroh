const CACHE_KEY = "sale_order_web";

function checkForStorage() {
    return typeof (Storage) !== "undefined"
}

function putData(data) {
    if (checkForStorage()) {
        sessionStorage.setItem(CACHE_KEY, JSON.stringify(data));
    }
}

function getData() {
    let dataStorage = [];
    if (checkForStorage()) {
        dataStorage = JSON.parse(localStorage.getItem(CACHE_KEY)) || [];
    }

    let data = {
        package: "<option value='' selected='' disabled=''>Package</option>",
        room_type: "<option value='' selected='' disabled=''>Room Type</option>",
        jamaah_count: 0,
        so_line: []
    }

    if (dataStorage.length > 0) {
        data = {
            package: dataStorage.package,
            room_type: dataStorage.room_type,
            jamaah_count: dataStorage.jamaah_count,
            so_line: dataStorage.so_line
        }
    }

    return data
}

export { getData, putData }