# -*- coding: utf-8 -*-

{
    'name': "Library Management System",
    'version': '18.0.4.0.0',
    'summary': 'A comprehensive module for managing library operations, including book tracking and member management.',
    'depends': ['base','web','sale_management','stock'],
    'category' : 'Education',
    'author': 'Harsh',
    'website': 'https://www.aktivsoftware.com',
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_product.xml',
        'data/ir_sequence_member.xml',
        'views/library_book_views.xml',
        'views/library_category_views.xml',
        'views/library_member_views.xml',
        'views/library_library_views.xml',
        'views/product_template_views.xml',
        'views/sale_order_quotation_views.xml',
        'views/bulk_upload_book_views.xml',
        'views/library_menus.xml',
        'views/sale_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
