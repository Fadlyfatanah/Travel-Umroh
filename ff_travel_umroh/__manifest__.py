# -*- coding: utf-8 -*-
{
    'name': "Travel Umroh",

    'description': """
        Module for management umroh
    """,

    'author': "Fadli Fatanah",
    'category': 'Travel Umroh',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'mrp', 'sale', 'account', 'website', 'ff_state_city'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_travel_package.xml',
        'data/product_attribute_data.xml',
        'views/view_travel_package.xml',
        'views/view_sale_order.xml',
        'views/view_product.xml',
        'views/view_res_partner.xml',
        'views/view_res_partner_title.xml',
        'views/action_view.xml',
        'views/menu_view.xml',
    ],
    'application': True,
}
