odoo.define("ff_travel_umroh.domain_country", function (require) {
    var FormRenderer = require("web.FormRenderer");
    var LoadData = FormRenderer.extend({
        loadProvinsi: function () {
            var idkota = document.getElementById("txt_kota");
            var idcabang = document.getElementById("txt_cabang");
            idkota.innerHTML = '<option value="">-Pilih Kota/Kabupaten-</option>';
            idcabang.innerHTML = '<option value="">-Pilih Cabang-</option>';
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4) {
                    if (this.status == 200) {
                        respon = xhttp.responseText;
                        var idprov = document.getElementById("txt_provinsi");
                        idprov.innerHTML = respon;
                    }
                }
            };
            xhttp.open("GET", "getprovinsi", true);
            xhttp.send();
        },
        loadKota: function () {
            var idkota = document.getElementById("txt_kota");
            var idcabang = document.getElementById("txt_cabang");
            idcabang.innerHTML = '<option value="">-load Cabang-</option>';
            idkota.innerHTML = '<option value="">-Pilih Kota/Kabupaten-</option>';
            var idprov = document.getElementById("txt_provinsi");
            var provPilih = idprov.value;
            if (provPilih != "") {
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function () {
                    if (this.readyState == 4) {
                        if (this.status == 200) {
                            respon = xhttp.responseText;
                            var idkota = document.getElementById("txt_kota");
                            idkota.innerHTML = respon;
                        }
                    }
                };
                var alamat = "getprovinsisubKota?prov=" + provPilih;
                xhttp.open("GET", alamat, true);
                xhttp.send();
            }
        },
        loadCabang: function () {
            var idcabang = document.getElementById("txt_cabang");
            idcabang.innerHTML = '<option value="">-Pilih Cabang-</option>';
            var idkota = document.getElementById("txt_kota");
            var kotaPilih = idkota.value;

            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4) {
                    if (this.status == 200) {
                        respon = xhttp.responseText;
                        var idcabang = document.getElementById("txt_cabang");
                        idcabang.innerHTML = respon;
                    }
                }
            };
            var alamat = "getprovinsisubKotasubCabang?kota=" + kotaPilih;
            xhttp.open("GET", alamat, true);
            xhttp.send();
        },
    });
    return LoadData;
});
