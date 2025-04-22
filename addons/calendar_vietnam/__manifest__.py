{
    'name': "Calendar Vietnam",
    'summary': "Tránh lên lịch sự kiện vào các ngày lễ Việt Nam",
    'description': """
        Module này mở rộng Odoo Calendar để ngăn lập lịch sự kiện vào các ngày lễ công cộng của Việt Nam
        và đề xuất các ngày thay thế.
    """,
    'author': "Đàm Mai",
    'version': '1.0',
    'depends': ['calendar', 'hr_holidays'],
    'data': [
        'wizards/suggest_date.xml',
        'views/calendar_views.xml',
        'data/data.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}