# -*- coding: utf-8 -*-
{
    'name': "hr-custom-employee-id",

    'summary': "View Employee Id",

    'description': """
        View employee id in employee form for hr module
    """,

    'author': "Bekern",
    'website': "http://www.bekern.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
}