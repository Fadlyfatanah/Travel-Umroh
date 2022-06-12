# -*- coding: utf-8 -*-
{
    'name': "Travel Umroh",

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
    'depends': ['base', 'mail', 'mrp', 'sale', 'crm', 'website', 'ff_state_city'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_travel_package.xml',
        'report/travel_package_report.xml',
        'views/css_ff_travel_umroh.xml',
        'views/views.xml',
        'views/action_view.xml',
        'views/assets.xml',
        'views/menu_view.xml',
        'views/menu_website.xml',
        'views/sale_portal_templates.xml',
        'views/travel_portal_templates.xml',
        'views/website_form_pendaftaran_view.xml',
    ],
    'qweb': [
        "/static/src/xml/counter.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
