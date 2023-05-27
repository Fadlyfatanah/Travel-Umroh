function deleteManifest(line){
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
    let alamat = "/shop/jamaah/delete?jamaah_id=" + jamaah_id
    xhttp.open("GET", alamat, true);
    xhttp.send();
    }
}