# -*- coding: utf-8 -*-
{
    'name': "loan_application",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'account',
                # 'ph_localization'
                # 'backend_theme',
                'sale',
                # 'loan_information',
                # 'brdc_account'
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/loan_client.xml',
        'views/application_wizard.xml',
        'views/res_users_view.xml',
        'views/local.xml',
        'views/res_company_view.xml',
        'views/internal_notes.xml',
        'views/interment_policy.xml',
        'views/Interment_order.xml',
        'views/ir_sequence.xml',
        'views/EIPP_view.xml',
        'report/policies.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    "images":['/static/img/address.png',],


}