# -*- coding: utf-8 -*-
{
    'name': "Travel Umroh Portal",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Module for management umroh
    """,

    'author': "Fadli Fatanah",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Travel Umroh',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'website_sale', 'ff_travel_umroh', 'ff_website_sale_without_payment'],

    # always loaded
    'data': [
        # 'views/css_ff_travel_umroh.xml',
        'views/sale_portal_templates.xml',
        'views/templates.xml',
        'views/ir_qweb_widget_templates.xml',
        'views/res_config_settings_views.xml',
        # 'views/travel_portal_templates.xml',
        # 'views/website_form_pendaftaran_view.xml',
        # 'views/website_sale_product_views.xml',
    ],
    'qweb': [
        
    ],
    'application': True,
}
