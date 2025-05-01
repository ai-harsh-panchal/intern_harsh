# -*- coding: utf-8 -*-

{
    'name': 'sale_order_customisation',
    'version': '18.0.1.0.0',
    'summary': 'customise manager approval workflow on the Sales Order module',
    'depends': ['base', 'web', 'sale_management', 'product', 'sale'],
    'category': 'Sale',
    'author': 'Harsh',
    'website': 'https://www.aktivsoftware.com',
    'data': [
        'security/ir.model.access.csv',
        'views/sale_manager_approval_view.xml',
        'views/config_setting_view.xml',
        'views/sale_order.xml',
        'data/approval_mail_template.xml',
        'report/sale_order_report.xml',
        'data/ir_cron.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
