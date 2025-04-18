# -*- coding: utf-8 -*-

{
    'name': "shop customisation",
    'version': '18.0.1.0.0',
    'summary': 'shop website customisation',
    'depends': ['base', 'web', 'sale_management', 'stock', 'website_sale', 'product', 'website', 'sale'],
    'category': 'Website',
    'author': 'Harsh',
    'website': 'https://www.aktivsoftware.com',
    'data': [
        'views/product_template_website.xml',
    ],
    "assets":
        {
            "web.assets_frontend":
                [
                    "/shop_customisation/static/src/js/add_to_cart.js",
                ],
        },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
