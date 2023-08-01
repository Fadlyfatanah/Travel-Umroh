# -*- coding: utf-8 -*-
{
    'name': "Travel Umrah Portal",
    'summary': """
        Modul untuk penjualan paket perjalanan umrah melalui portal
    """,
    'author': "Fadli Fatanah",
    'website': "https://fadlyfatanah.github.io/",
    'category': 'Travel Umrah',
    'version': '14.0.0.1.0',
    'depends': ['base', 'website', 'website_sale', 'ff_travel_umrah', 'ff_website_sale_payment_settings'],
    'data': [
        'views/ir_qweb_widget_templates.xml',
        'views/jamaah_website_templates.xml',
        'views/res_config_settings_views.xml',
        'views/sale_portal_templates.xml',
    ],
    'application': True,
    "license": "LGPL-3",
}
