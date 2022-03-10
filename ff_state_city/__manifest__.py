# -*- coding: utf-8 -*-
{
    'name': 'City',
    'version': '0.1',
    'author': 'Fadli Fatanah',
    'category': 'Master',
    'website': '',
    'summary': 'Kota Kecamatan Kelurahan (Indonesia)',
    'description': '''
        Data Kota Kecamatan Kelurahan (Indonesia)
    ''',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/city_view.xml',
        'views/res_view.xml',
        # 'views/branch_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}