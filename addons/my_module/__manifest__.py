{
    'name': 'My Module',
    'version': '1.0',
    'summary': 'demo module',
    'description': 'Chi tiết về module của dũng',
    'category': 'Custom',
    'author': 'Phạm Ngọc Anh Dũng',
    'license': 'LGPL-3',
    'website': 'https://web.facebook.com/dung.pham.514768/',
    'depends': ['base'],  
    'data': [
        # 'security/security.xml'
        'views/my_model_views.xml',
        'security/ir.model.access.csv',
        'data/data.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

