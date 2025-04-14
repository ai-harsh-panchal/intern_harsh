# -*- coding: utf-8 -*-

{
    'name': 'CRM Customisation',
    'version': '18.0.1.0.0',
    'summary': 'Enhancements to CRM and Sales Order Management',
    'description': """
     this module is for custom enhancements to the CRM and Sales Order management processes
    """,
    'author': 'harsh',
    'website': 'https://www.aktivsoftware.com',
    'category': 'CRM',
    'depends': ['calendar', 'contacts', 'sale', 'mrp', 'project', 'stock', 'crm', 'stock', 'account'],
    'data': [
        'views/sale_order.xml',
        'views/account_move.xml',
        'views/project_project.xml',
        'views/stock_picking.xml',
        'views/mrp_production.xml',
    ],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
