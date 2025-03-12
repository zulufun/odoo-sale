from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _name = 'custom.sale.order.line'
    _description = 'Chi tiết đơn hàng bán'
    
    order_id = fields.Many2one('custom.sale.order', string='Đơn hàng', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Sản phẩm', required=True)
    name = fields.Text(string='Mô tả', required=True)
    product_uom_qty = fields.Float(string='Số lượng', default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Đơn vị đo lường')
    price_unit = fields.Float(string='Đơn giá')
    tax_id = fields.Many2many('account.tax', string='Thuế')
    discount = fields.Float(string='Chiết khấu (%)', default=0.0)
    
    currency_id = fields.Many2one(related='order_id.currency_id')
    price_subtotal = fields.Monetary(string='Thành tiền', compute='_compute_amount', store=True)
    price_tax = fields.Monetary(string='Thuế', compute='_compute_amount', store=True)
    price_total = fields.Monetary(string='Tổng cộng', compute='_compute_amount', store=True)
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.price_unit = self.product_id.list_price
            self.product_uom = self.product_id.uom_id
    
    @api.depends('product_uom_qty', 'price_unit', 'tax_id', 'discount')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(
                price, 
                line.order_id.currency_id, 
                line.product_uom_qty, 
                product=line.product_id
            )
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_subtotal': taxes['total_excluded'],
                'price_total': taxes['total_included'],
            })