import { Component, tags } from "@odoo/owl";

const COUNT_TEMPLATE = tags.xml`
<input type="number" id="jamaah_count" class="o_input o_product_qty form-control text-right" value="0" min="1"/>`;

export class JamaahCount extends Component{
    static template = COUNT_TEMPLATE;
}