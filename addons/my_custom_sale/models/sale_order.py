from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class SaleOrder(models.Model):
    _name = 'custom.sale.order'
    _description = 'Đơn hàng bán'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_order desc, id desc'
    
    name = fields.Char(string='Mã đơn hàng', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Khách hàng', required=True)
    date_order = fields.Datetime(string='Ngày đặt hàng', default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', string='Nhân viên bán hàng', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Công ty', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Bản thảo'),
        ('sent', 'Đã gửi'),
        ('sale', 'Đơn hàng bán'),
        ('done', 'Hoàn thành'),
        ('cancel', 'Hủy bỏ'),
    ], string='Trạng thái', default='draft', tracking=True)
    
    order_line = fields.One2many('custom.sale.order.line', 'order_id', string='Chi tiết đơn hàng')
    note = fields.Text(string='Ghi chú')
    
    amount_untaxed = fields.Monetary(string='Tổng tiền chưa thuế', compute='_compute_amounts', store=True)
    amount_tax = fields.Monetary(string='Thuế', compute='_compute_amounts', store=True)
    amount_total = fields.Monetary(string='Tổng tiền', compute='_compute_amounts', store=True)
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('custom.sale.order') or _('New')
        return super(SaleOrder, self).create(vals)
    
    @api.depends('order_line.price_subtotal')
    def _compute_amounts(self):
        for order in self:
            amount_untaxed = sum(line.price_subtotal for line in order.order_line)
            amount_tax = sum(line.price_tax for line in order.order_line)
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })
    
    def action_confirm(self):
        self.write({'state': 'sale'})
    
    def action_cancel(self):
        self.write({'state': 'cancel'})
    
    def action_draft(self):
        self.write({'state': 'draft'})
    
    def action_done(self):
        self.write({'state': 'done'})