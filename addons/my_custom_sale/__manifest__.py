{
    'name': 'Custom Sales Module',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Module bán hàng tùy chỉnh',
    'description': """
        Module này mở rộng và tùy chỉnh chức năng bán hàng của Odoo.
    """,
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}