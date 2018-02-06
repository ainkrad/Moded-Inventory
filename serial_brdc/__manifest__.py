# -*- coding: utf-8 -*-
{
    'name': "serial_brdc",

    'summary': """A Small Description""",

    'description': """
        No purpose at all
    """,

    'author': "MGC",
    'website': "http://www.mutigroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/inherited_stock_production_lot.xml',
        'views/inherited_product_template_view.xml',
        'views/inherited_product_template_tree_view.xml',
        'views/inherited_stock_quant.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}