from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

SALE_ORDER_STATE = [
    ('draft', "Báo giá"),
    ('sent', "Đã gửi báo giá"),
    ('sale', "Đơn hàng"),
    ('done', "Hoàn thành"),
    ('cancel', "Hủy"),
]

class SaleOrder(models.Model):
    _name = 'simple.sale.order'
    _description = "Đơn hàng"
    _order = 'date_order desc, id desc'

    name = fields.Char(
        string="Mã đơn hàng",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))
    
    partner_id = fields.Many2one(
        'res.partner',
        string="Khách hàng",
        required=True, index=True)
        
    state = fields.Selection(
        selection=SALE_ORDER_STATE,
        string="Trạng thái",
        readonly=True, copy=False, index=True,
        default='draft')
        
    date_order = fields.Datetime(
        string="Ngày đặt hàng",
        required=True, copy=False,
        default=fields.Datetime.now)
        
    user_id = fields.Many2one(
        'res.users',
        string="Nhân viên bán hàng",
        default=lambda self: self.env.user)
        
    company_id = fields.Many2one(
        'res.company',
        string="Công ty",
        required=True, index=True,
        default=lambda self: self.env.company)
        
    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        string="Tiền tệ")
        
    order_line = fields.One2many(
        'simple.sale.order.line',
        'order_id',
        string="Chi tiết đơn hàng",
        copy=True)
        
    note = fields.Text(string="Ghi chú")
    
    amount_untaxed = fields.Monetary(
        string="Tổng tiền chưa thuế",
        compute='_compute_amounts',
        store=True)
        
    amount_tax = fields.Monetary(
        string="Thuế",
        compute='_compute_amounts',
        store=True)
        
    amount_total = fields.Monetary(
        string="Tổng tiền",
        compute='_compute_amounts',
        store=True)
    
    @api.depends('order_line.price_subtotal')
    def _compute_amounts(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.amount_untaxed = amount_untaxed
            order.amount_tax = amount_tax
            order.amount_total = amount_untaxed + amount_tax
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('simple.sale.order') or _('New')
        return super().create(vals_list)
    
    def action_confirm(self):
        for order in self:
            if order.state in ('draft', 'sent'):
                order.state = 'sale'
    
    def action_cancel(self):
        for order in self:
            order.state = 'cancel'
    
    def action_done(self):
        for order in self:
            order.state = 'done'
    
    def action_draft(self):
        for order in self:
            order.state = 'draft'
    
    def action_quotation_send(self):
        for order in self:
            order.state = 'sent'
