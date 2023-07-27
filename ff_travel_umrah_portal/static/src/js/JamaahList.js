function selectJamaah(id_div, idJamaah) {
    let input = document.getElementById(`jamaah_${idJamaah}`);
    if (input.value == ''){
        input.value = 'on'
        id_div.setAttribute("class", "card")
        id_div.setAttribute("style", "border-width: 3px; border-color: #3AADAA;")
    }
    else if (input.value == 'on'){
        input.value = ''
        id_div.setAttribute("class", "card border border-secondary")
        id_div.setAttribute("style", "")
    }
}

function getSelection(idRow) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange =
        function () {
            if (this.readyState == 4 && this.status == 200) {
                let respon_text = xhttp.responseText;
                let respon = JSON.parse(respon_text);
                let row = document.getElementById(idRow);
                getJamaahList(row, respon)
            }
        };
    let alamat = "/shop/jamaah/selection/list";
    xhttp.open("GET", alamat, true);
    xhttp.send();
}

function getJamaahList(row, respon) {
    let jamaahRow = "";
    for (jamaah of respon.jamaah_ids) {
        let id = jamaah["id"];
        let jamaahInput = `<input id="jamaah_${id}" type="hidden" name="${id}"/>`;
        // jamaahWidget = `<t t-set="contact" t-value="${id}"/>`;
        let jamaahWidgets = `<div onclick="selectJamaah(this, ${id})" class="card border border-secondary"><div class="card-body" style="min-height: 70px;"><address class="mb-0" itemscope="itemscope" itemtype="http://schema.org/Organization"><div><span itemprop="name">${jamaah["name"]}</span></div><div class="css_editable_mode_hidden"><div><i class="fa fa-address-card fa-fw" role="img" aria-label="KTP" title="KTP"></i><span class="o_force_ltr" itemprop="ktp_no">${jamaah["ktp_no"]}</span></div></div><div itemprop="address" itemscope="itemscope" itemtype="http://schema.org/PostalAddress"><div><i class="fa fa-mobile fa-fw" role="img" aria-label="Mobile" title="Mobile"></i> <span class="o_force_ltr" itemprop="telephone">${jamaah["mobile"]}</span></div></div></address></div></div>`;
        jamaahRow += `<div class="col-lg-12 one_kanban mb-2">${jamaahInput}${jamaahWidgets}</div>`;
    }
    row.innerHTML = jamaahRow;
}

getSelection("selection_name_div");
