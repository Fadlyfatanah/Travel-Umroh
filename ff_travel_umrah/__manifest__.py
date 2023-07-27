# -*- coding: utf-8 -*-
{
    'name': "Travel Umrah",
    'summary': """
            Modul untuk penjualan paket perjalanan umrah
    """,
    'author': "Fadli Fatanah",
    'website': "https://fadlyfatanah.github.io/",
    'category': 'Travel Umrah',
    'version': '14.0.0.1.0',
    'depends': ['base', 'mail', 'mrp', 'sale', 'account', 'website'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_module_category_data.xml',
        'data/ir_sequence_travel_package.xml',
        'data/product_attribute_data.xml',
        'views/product_view.xml',
        'views/res_clothes_size_view.xml',
        'views/res_education_view.xml',
        'views/res_marital_status_view.xml',
        'views/res_partner_title_view.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/travel_package_view.xml',
        'views/action_view.xml',
        'views/menu_view.xml',
    ],
    'application': True,
    "license": "LGPL-3",
}
