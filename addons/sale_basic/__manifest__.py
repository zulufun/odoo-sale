{
    'name': 'Bán hàng đơn giản',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Module bán hàng đơn giản',
    'description': """
Module bán hàng đơn giản hóa từ module sale của Odoo.
Chứa các chức năng bán hàng cơ bản nhất.
    """,
    'depends': [
        'base',
        'sale',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sale_sequence.xml',
        'views/sale_order_views.xml',
        'views/sale_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'icon': '/sale_basic/static/description/mta.png',
}
