from odoo import models, fields

class Employee(models.Model):
    _inherit = 'hr.employee'  # Kế thừa model hr.employee để thao tác trên employee