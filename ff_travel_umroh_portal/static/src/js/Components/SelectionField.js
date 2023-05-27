
odoo.define('ff_travel_umroh.selection_field', function (require) {
    'use strict';

    const { Component, tags } = owl;

    const SELECTION_TEMPLATE = tags.xml`
    <select name="props.name" class="form-control">
        <option value="" selected="" disabled="">props.label</option>
    </select>`;

    // function SelectionField({members}){
    //     members.map(() => tags.xml`
    //         <option t-att-value="package.id">
    //             <t t-esc="package.name"/>
    //         </option>
    //     `)
    // }
    class SelectionField extends Component {
        static template = SELECTION_TEMPLATE;

        // xml`
        // <option t-att-value="package.id">
        //     <t t-esc="package.name"/>
        // </option>`;

    }

    return SelectionField();

});

// export default SelectionField