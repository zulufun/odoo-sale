from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _name = 'simple.sale.order.line'
    _description = "Chi tiết đơn hàng"
    _order = 'order_id, sequence, id'

    order_id = fields.Many2one(
        'simple.sale.order',
        string="Đơn hàng",
        required=True, ondelete='cascade', index=True)
        
    sequence = fields.Integer(string="Thứ tự", default=10)
    
    product_id = fields.Many2one(
        'product.product',
        string="Sản phẩm",
        required=True,
        domain=[('sale_ok', '=', True)])
        
    name = fields.Text(
        string="Mô tả",
        required=True)
        
    product_uom_qty = fields.Float(
        string="Số lượng",
        digits='Product Unit of Measure',
        default=1.0,
        required=True)
        
    product_uom = fields.Many2one(
        'uom.uom',
        string="Đơn vị",
        required=True)
        
    price_unit = fields.Float(
        string="Đơn giá",
        digits='Product Price',
        required=True)
        
    tax_id = fields.Many2many(
        'account.tax',
        string="Thuế",
        domain=[('type_tax_use', '=', 'sale')])
        
    discount = fields.Float(
        string="Chiết khấu (%)",
        digits='Discount',
        default=0.0)
        
    currency_id = fields.Many2one(
        related='order_id.currency_id',
        depends=['order_id'],
        store=True, string='Tiền tệ')
        
    company_id = fields.Many2one(
        related='order_id.company_id',
        string='Công ty',
        store=True, index=True)
        
    price_subtotal = fields.Monetary(
        string="Thành tiền",
        compute='_compute_amount',
        store=True)
        
    price_tax = fields.Float(
        string="Thuế",
        compute='_compute_amount',
        store=True)
        
    price_total = fields.Monetary(
        string="Tổng cộng",
        compute='_compute_amount',
        store=True)
    
    @api.depends('product_uom_qty', 'price_unit', 'tax_id', 'discount')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(
                price, line.currency_id, line.product_uom_qty,
                product=line.product_id, partner=line.order_id.partner_id
            )
            line.price_subtotal = taxes['total_excluded']
            line.price_tax = taxes['total_included'] - taxes['total_excluded']
            line.price_total = taxes['total_included']
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if not self.product_id:
            return
        
        self.name = self.product_id.name
        self.product_uom = self.product_id.uom_id
        self.price_unit = self.product_id.list_price
