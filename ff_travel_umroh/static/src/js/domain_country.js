// odoo.define("ff_travel_umroh.domain_country", function (require) {
//     var FormRenderer = require("web.FormRenderer");
//     var LoadData = FormRenderer.extend({
//         loadProvinsi: function () {
//             var idkota = document.getElementById("txt_kota");
//             var idcabang = document.getElementById("txt_cabang");
//             idkota.innerHTML = '<option value="">-Pilih Kota/Kabupaten-</option>';
//             idcabang.innerHTML = '<option value="">-Pilih Cabang-</option>';
//             var xhttp = new XMLHttpRequest();
//             xhttp.onreadystatechange = function () {
//                 if (this.readyState == 4) {
//                     if (this.status == 200) {
//                         respon = xhttp.responseText;
//                         var idprov = document.getElementById("txt_provinsi");
//                         idprov.innerHTML = respon;
//                     }
//                 }
//             };
//             xhttp.open("GET", "getprovinsi", true);
//             xhttp.send();
//         },
//         loadKota: function () {
//             var idkota = document.getElementById("txt_kota");
//             var idcabang = document.getElementById("txt_cabang");
//             idcabang.innerHTML = '<option value="">-load Cabang-</option>';
//             idkota.innerHTML = '<option value="">-Pilih Kota/Kabupaten-</option>';
//             var idprov = document.getElementById("txt_provinsi");
//             var provPilih = idprov.value;
//             if (provPilih != "") {
//                 var xhttp = new XMLHttpRequest();
//                 xhttp.onreadystatechange = function () {
//                     if (this.readyState == 4) {
//                         if (this.status == 200) {
//                             respon = xhttp.responseText;
//                             var idkota = document.getElementById("txt_kota");
//                             idkota.innerHTML = respon;
//                         }
//                     }
//                 };
//                 var alamat = "getprovinsisubKota?prov=" + provPilih;
//                 xhttp.open("GET", alamat, true);
//                 xhttp.send();
//             }
//         },
//         loadCabang: function () {
//             var idcabang = document.getElementById("txt_cabang");
//             idcabang.innerHTML = '<option value="">-Pilih Cabang-</option>';
//             var idkota = document.getElementById("txt_kota");
//             var kotaPilih = idkota.value;

//             var xhttp = new XMLHttpRequest();
//             xhttp.onreadystatechange = function () {
//                 if (this.readyState == 4) {
//                     if (this.status == 200) {
//                         respon = xhttp.responseText;
//                         var idcabang = document.getElementById("txt_cabang");
//                         idcabang.innerHTML = respon;
//                     }
//                 }
//             };
//             var alamat = "getprovinsisubKotasubCabang?kota=" + kotaPilih;
//             xhttp.open("GET", alamat, true);
//             xhttp.send();
//         },
//     });
//     return LoadData;
// });

loadNegara();
function loadNegara(){
    var idkota = document.getElementById('txt_kota');
    var idprovinsi = document.getElementById('txt_provinsi');
    idkota.innerHTML = '<option value="">-Pilih Kota/Kabupaten-</option>'
    idprovinsi.innerHTML = '<option value="">-Pilih Provinsi-</option>'
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange =
        function () {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    respon = xhttp.responseText;
                    var idnegara = document.getElementById('txt_negara');
                    idnegara.innerHTML = respon;
                }
            }
        };
    xhttp.open("GET", "/pendaftaran/data-diri/getnegara", true);
    xhttp.send();
}
function pilihProvinsi() {
    var idkota = document.getElementById('txt_kota');
    var idprovinsi = document.getElementById('txt_provinsi');
    idprovinsi.innerHTML = '<option value="">-Pilih Provinsi-</option>'
    idkota.innerHTML = '<option value="">-Pilih Kota/Kabupaten-</option>'
    var idnegara = document.getElementById('txt_negara');
    var negaraPilih = idnegara.value;
    if (negaraPilih != "") {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange =
            function () {
                if (this.readyState == 4) {
                    if (this.status == 200) {
                        respon = xhttp.responseText;
                        var idprovinsi = document.getElementById('txt_provinsi');
                        idprovinsi.innerHTML = respon;
                    }
                }
            };
        var alamat = "/pendaftaran/data-diri/getNegarasubProvinsi?negara=" + negaraPilih
        xhttp.open("GET", alamat, true);
        xhttp.send();
    }
}
function pilihKota() {
    var idprovinsi = document.getElementById('txt_provinsi');
    var provinsiPilih = idprovinsi.value;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange =
        function () {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    respon = xhttp.responseText;
                    var idkota = document.getElementById('txt_kota');
                    idkota.innerHTML = respon;
                }
            }
        };
    var alamat = "/pendaftaran/data-diri/getNegarasubProvinsisubKota?provinsi=" + provinsiPilih
    xhttp.open("GET", alamat, true);
    xhttp.send();
}