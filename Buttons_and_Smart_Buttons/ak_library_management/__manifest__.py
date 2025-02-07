# -*- coding: utf-8 -*-

{
    'name': "Library Management System",
    'version': '18.0.4.0.0',
    'summary': 'A comprehensive module for managing library operations, including book tracking and member management.',
    'depends': ['base','web','stock','product'],
    'category' : 'Education',
    'author': 'Harsh',
    'website': 'https://www.aktivsoftware.com',
    'data': [
        'security/ir.model.access.csv',
        'views/book_view.xml',
        'views/categories_view.xml',
        'views/member_view.xml',
        'views/library_view.xml',
        'views/inherit_product_template_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
