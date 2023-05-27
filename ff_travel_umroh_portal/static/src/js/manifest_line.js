const CACHE_KEY = "sale_order_web";

function createTable(row) {
  row = parseInt(row.value);
  if (row > 0) {
    let head = "<th>Jamaah</th><th>Identity Number</th><th>Gender</th><th>Age</th><th>Mahram</th><th>Notes</th><th></th>";
    let body = "";
    for (let i = 1; i <= row; i++) {
      body += renderBody(i);
    }
    let thead = document.getElementById("thead");
    let tbody = document.getElementById("tbody");
    if (thead && tbody) {
      thead.innerHTML = head;
      tbody.innerHTML = body;
      let rows = document.getElementsByName("jamaah")
      for (let i = 1; i < rows.length + 1; i++) {
        loadData(i);
      }
    }
  }

}

function renderBody(idRow) {
  let selectJamaah = createElementSelect("jamaah", `selectJamaah(${idRow})`);
  let ktp = `<td><span name="ktp_no"></span></td>`;
  let gender = `<td><span name="gender"></span></td>`;
  let age = `<td><span name="age"></span></td>`;
  let selectMahram = createElementSelect("mahram");
  let note = `<td><input name="note" type="text" value=""/></td>`;
  let buttonDelete = `<td class="o_list_record_remove"><button name="delete" class="fa fa-trash" onclick="deleteRow(this)"></button></td>`;
  let body = `<tr id=${idRow} name="row_table">` + selectJamaah + ktp + gender + age + selectMahram + note + buttonDelete + "</tr>"
  return body
}

function loadData(idRow) {
  listJamaah = []
  let rows = document.getElementsByName("jamaah")
  for (item of rows) {
    value_row = item.childNodes[0].attributes[0].value
    if (value_row != "") {
      listJamaah.push(parseInt(item.childNodes[0].value))
    }
  }
  loadJamaah(idRow, listJamaah);
  loadMahram(idRow);
}

function loadJamaah(idRow, listJamaah = []) {
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange =
    function () {
      if (this.readyState == 4) {
        if (this.status == 200) {
          respon = xhttp.responseText;
          let row = document.getElementById(idRow);
          row.childNodes[0].childNodes[0].innerHTML = respon;
        }
      }
    };
  let alamat = "/pendaftaran/getListJamaah?listJamaah=" + listJamaah
  xhttp.open("GET", alamat, true);
  xhttp.send();
}

function loadMahram(idRow) {
  let row = document.getElementById(idRow);
  let jamaah_id = row.childNodes[0].childNodes[0].value;
  if (jamaah_id != "") {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange =
      function () {
        if (this.readyState == 4) {
          if (this.status == 200) {
            respon = xhttp.responseText;
            row.childNodes[4].childNodes[0].innerHTML = respon;
          }
        }
      };
    let alamat = "/pendaftaran/getListMahram?jamaah_id=" + jamaah_id
    xhttp.open("GET", alamat, true);
    xhttp.send();
  }
}

function createElementSelect(name, event = "") {
  let upperName = name[0].toUpperCase() + name.substring(1);
  let optionElement = `<option value="" selected="" disabled="">${upperName}</option>`;
  let selectElement = `<td><select name="${name}" onchange=${event}>` + optionElement + `</select></td>`;
  return selectElement
}

function selectJamaah(idRow) {
  let row = document.getElementById(idRow);
  let jamaah_id = row.childNodes[0].childNodes[0].value;
  if (jamaah_id != "") {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange =
      function () {
        if (this.readyState == 4 && this.status == 200) {
          respon = xhttp.responseText;
          parser = new DOMParser();
          xmlDoc = parser.parseFromString(respon, "text/xml");
          let ktp = xmlDoc.getElementsByTagName("div")[0].innerHTML
          let gender = xmlDoc.getElementsByTagName("div")[1].innerHTML
          let age = xmlDoc.getElementsByTagName("div")[2].innerHTML
          row.childNodes[1].childNodes[0].innerHTML = ktp
          row.childNodes[2].childNodes[0].innerHTML = gender
          row.childNodes[3].childNodes[0].innerHTML = age
          loadData(idRow);
        }
      };
    let alamat = "/pendaftaran/getDetailJamaah?jamaah_id=" + jamaah_id
    xhttp.open("GET", alamat, true);
    xhttp.send();
  }
}

function deleteRow(idRow) {
  document.getElementById('tbody').removeChild(idRow.parentNode.parentNode)
  document.getElementById('jamaah_count').value = document.getElementsByName('row_table').length
}

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
    dataStorage = JSON.parse(sessionStorage.getItem(CACHE_KEY)) || [];
  }

  let data = {
    package: '<option value="" selected="" disabled="">Package</option>',
    room_type: `<option value="" selected="" disabled="">Room Type</option>`,
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

function saveData() {
  let data_so_line = [];
  document.getElementsByName('row_table').innerHTML.map((row) => {
    data_so_line.push({
      "jamaah": row.getElementsByName("jamaah")[0].querySelector('[selected=""]').innerHTML,
      "identity_number": row.getElementsByName("ktp_no")[0].innerHTML,
      "gender": row.getElementsByName("gender")[0].innerHTML,
      "age": row.getElementsByName("age")[0].innerHTML,
      "mahram": row.getElementsByName("mahram")[0].querySelector('[selected=""]').innerHTML,
      "note": row.getElementsByName("note")[0].innerHTML
    })
  })

  let data_so = {
    package: document.getElementById('package').querySelector('[selected=""]').innerHTML,
    room_type: document.getElementById('room_type').querySelector('[selected=""]').innerHTML,
    jamaah_count: document.getElementById('jamaah_count').querySelector('[selected=""]').innerHTML,
    so_line: data_so_line
  }
  putData(data_so);
}