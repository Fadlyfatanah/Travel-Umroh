odoo.define('ff_travel_umroh_portal.sale_order', function (require) {
    'use strict';

    const { Component, mount, tags, useState } = owl;
    var SelectionField = require("ff_travel_umroh_portal.selection_field");

    const SO_TEMPLATE = tags.xml`
    <h1>Tes Owl</h1>
    `;
    // <div class="col col-12" string="Personal Data">
    //     <SelectionField label="Jamaah"/>
    //     <SelectionField label="Mahram"/>
    // </div>
    // <JamaahCount/>
    // <SaleOrderLine/>
    class SaleOrder extends Component {
        static template = SO_TEMPLATE;
        // static components = { SelectionField };
        state = useState({
            package: ["<option value='' selected='' disabled=''>Package</option>"],
            room_type: ["<option value='' selected='' disabled=''>Room Type</option>"],
            jamaah_count: 0,
            so_line: []
        })
    }

    const SO = new SaleOrder();
    SO.mount(document.getElementById("pendaftaran_jamaah_form"));
    // mount(SaleOrder, document.getElementById("pendaftaran_jamaah_form"));

    // Object.assign(SaleOrder, { 
    //     template: "ff_travel_umroh_portal.sale_order" 
    // }); 
});