{
    'name': 'Custom Sales Inventory View',
    'version': '1.0',
    'summary': 'View products in inventory',
    'description': 'Hiển thị sản phẩm có trong kho hàng',
    'category': 'Sales',
    'author': 'Nguyên',
    'license': 'LGPL-3',
    'website': 'https://www.odoo.com',
    'depends': ['base', 'sale', 'stock'],
    'data': [
        'views/product_inventory_views.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}