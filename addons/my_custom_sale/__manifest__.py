{
    'name': 'Custom Sales',
    'version': '1.0',
    'summary': 'Quản lý bán hàng',
    'description': """
        Module quản lý bán hàng cho Odoo
        - Quản lý đơn hàng
        - Báo cáo bán hàng
        - Quản lý khách hàng
    """,
    'category': 'Sales',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'product', 'account'],
    'data': [
        'security/sales_security.xml',
        'security/ir.model.access.csv',
        'views/sale_views.xml',
        'views/sale_order_views.xml',
        'views/sale_report_views.xml',
        'views/menu_views.xml',
        'report/sale_report_templates.xml',
        'data/sale_data.xml',
    ],
    'demo': [
        'data/sale_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}