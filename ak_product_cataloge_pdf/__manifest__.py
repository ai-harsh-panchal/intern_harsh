# -*- coding: utf-8 -*-

{
    'name': "product_cataloge_pdf",
    'version': '18.0.1.0.0',
    'summary': 'Application for print product details as a cataloge report',
    'depends': ['base', 'web', 'sale_management', 'stock', 'product', 'sale'],
    'category': 'Sale',
    'author': 'Harsh',
    'website': 'https://www.aktivsoftware.com',
    'data': [
        'security/ir.model.access.csv',
        'report/product_catalog_report_template.xml',
        'report/product_catalog_report_action.xml',
        'wizard/product_catlog_wizard_view.xml',
        'views/sale_menu.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
