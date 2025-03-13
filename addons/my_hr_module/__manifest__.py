{
    'name': 'My HR Module',
    'version': '1.0',
    'summary': 'Demo hr module',
    'description': 'Lấy dữ liệu từ module hr và hiển thị lên view',
    'category': 'Custom',
    'author': 'Nguyên',
    'license': 'LGPL-3',
    'website': 'https://www.odoo.com',
    'depends': ['base', 'hr'],  
    'data': [
        'views/employee_views.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}