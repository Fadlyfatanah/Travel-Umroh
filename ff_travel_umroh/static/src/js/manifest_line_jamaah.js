import React from 'react';
import ReactDOM from 'react-dom/client';

function createTable(row){
    val = parseInt(row.value)
    if (val > 0){
        renderTable(val);
    }
}

function renderTable(val){
	var head = "<th>Jamaah</th><th>Identity Number</th><th>Gender</th><th>Age</th><th>Mahram</th><th>Notes</th><th></th>";
    var body = "";
    for (var i = 1; i <= val; i++){
        body += renderBody(i);
    }
    var thead = document.getElementById("thead");
    var tbody = document.getElementById("tbody");
    if (thead && tbody){
        thead.innerHTML = head;
        tbody.innerHTML = body;
        var rows =  document.getElementsByName("jamaah")
        for(var i = 1; i < rows.length + 1; i++){
            loadData(i);
        }
    }

}

function renderBody(idRow) {
	// var dataJamaah = loadJamaah;
	// var dataMahram = loadMahram;
	var selectJamaah = createElementSelect("jamaah", `selectJamaah(${idRow})`);
	var ktp = `<td><span name="ktp_no"></span></td>`;
	var gender = `<td><span name="gender"></span></td>`;
	var age = `<td><span name="age"></span></td>`;
	var selectMahram = createElementSelect("mahram", "");
    var note = `<td><input name="note" type="text"/></td>`;
	var buttonDelete = `<td class="o_list_record_remove"><button name="delete" class="fa fa-trash" onclick="deleteRow(this)"></button></td>`;
	var body = `<tr id=${idRow} name="row_table">` + selectJamaah + ktp + gender + age + selectMahram + note + buttonDelete + "</tr>"
	return body
}

function loadData(idRow){
    listJamaah = []
    var rows =  document.getElementsByName("jamaah")
    for(item of rows){
        value_row = item.childNodes[0].attributes[0].value
        if(value_row != ""){
            listJamaah.push(parseInt(item.childNodes[0].value))
        }
    }
    loadJamaah(idRow, listJamaah);
    loadMahram(idRow);
}

function loadJamaah(idRow, listJamaah=[]){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange =
        function () {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    respon = xhttp.responseText;
                    var row = document.getElementById(idRow);
                    row.childNodes[0].childNodes[0].innerHTML = respon;
                }
            }
        };
        var alamat = "/pendaftaran/getListJamaah?listJamaah=" + listJamaah
        xhttp.open("GET", alamat, true);
        xhttp.send();
    }
    
function loadMahram(idRow) {
    var row = document.getElementById(idRow);
    var jamaah_id = row.childNodes[0].childNodes[0].value;
    if (jamaah_id != "") {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange =
        function () {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    respon = xhttp.responseText;
                    row.childNodes[4].childNodes[0].innerHTML = respon;
                }
                }
            };
        var alamat = "/pendaftaran/getListMahram?jamaah_id=" + jamaah_id
        xhttp.open("GET", alamat, true);
        xhttp.send();
    }
}

function createElementSelect(name, onchange){
    var upperName = name[0].toUpperCase() + name.substring(1)
    var text = `<td><select name="${name}" onchange=${onchange}><option value="" selected="" disabled="">${upperName}</option></select></td>`;
    return text
}

function selectJamaah(idRow){
    var row = document.getElementById(idRow);
    var jamaah_id = row.childNodes[0].childNodes[0].value;
    if (jamaah_id != "") {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange =
            function () {
                if (this.readyState == 4 && this.status == 200) {
                    respon = xhttp.responseText;
                    parser = new DOMParser();
                    xmlDoc = parser.parseFromString(respon,"text/xml");
                    var ktp = xmlDoc.getElementsByTagName("div")[0].innerHTML
                    var gender = xmlDoc.getElementsByTagName("div")[1].innerHTML
                    var age = xmlDoc.getElementsByTagName("div")[2].innerHTML
                    row.childNodes[1].childNodes[0].innerHTML = ktp
                    row.childNodes[2].childNodes[0].innerHTML = gender
                    row.childNodes[3].childNodes[0].innerHTML = age
                    loadData(idRow);
                }
            };
        var alamat = "/pendaftaran/getDetailJamaah?jamaah_id=" + jamaah_id
        xhttp.open("GET", alamat, true);
        xhttp.send();
    }
}

function deleteRow(idRow){
    document.getElementById('tbody').removeChild(idRow.parentNode.parentNode)
    document.getElementById('jamaah_count').value = document.getElementsByName('row_table').length
}

function testReact(){
    const root = ReactDOM.createRoot(document.getElementById('demo'));
    root.render(<h1>Hello, world!</h1>);
}