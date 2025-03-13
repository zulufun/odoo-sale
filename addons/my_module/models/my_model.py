from odoo import models, fields

class MyModel(models.Model):
    _name = 'my'
    _description = 'Mô tả Model'

    name = fields.Char(string='Họ và tên', required=True)
    age = fields.Integer(string='tuổi')
    bio = fields.Text(string='tiểu sử')
    email = fields.Char(string='Email')

