# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Sales Inventory View',
    'version': '1.0',
    'category': 'Sales/Sales',
    'summary': 'Custom view for inventory products in sales',
    'description': """
This module extends the Sales application to allow viewing products in inventory.
    """,
    'depends': [
        'sale',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_inventory_views.xml',
        'views/custom_sale_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}