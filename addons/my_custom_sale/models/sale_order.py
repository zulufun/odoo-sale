from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    # Thêm các trường mới
    custom_reference = fields.Char('Mã tham chiếu tùy chỉnh')
    priority = fields.Selection([
        ('0', 'Thấp'),
        ('1', 'Trung bình'),
        ('2', 'Cao'),
    ], string='Mức độ ưu tiên', default='1')
    expected_delivery_date = fields.Date('Ngày giao hàng dự kiến')
    customer_notes = fields.Text('Ghi chú khách hàng')
    
    # Trường tính toán
    total_weight = fields.Float(string='Tổng khối lượng', compute='_compute_total_weight', store=True)
    
    @api.depends('order_line.product_id', 'order_line.product_uom_qty')
    def _compute_total_weight(self):
        for order in self:
            total_weight = 0.0
            for line in order.order_line:
                total_weight += line.product_id.weight * line.product_uom_qty
            order.total_weight = total_weight
    
    @api.onchange('partner_id')
    def _onchange_set_custom_reference(self):
        if self.partner_id:
            self.custom_reference = f"SO-{self.partner_id.id}-{datetime.now().strftime('%Y%m%d')}"
    
    @api.constrains('expected_delivery_date')
    def _check_expected_delivery_date(self):
        for order in self:
            if order.expected_delivery_date and order.expected_delivery_date < fields.Date.today():
                raise ValidationError(_("Ngày giao hàng dự kiến không thể là ngày trong quá khứ!"))
    
    def action_confirm(self):
        # Ghi đè phương thức xác nhận đơn hàng
        for order in self:
            if not order.custom_reference:
                raise UserError(_("Vui lòng nhập mã tham chiếu tùy chỉnh trước khi xác nhận đơn hàng!"))
        return super(SaleOrder, self).action_confirm()

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    # Thêm trường vào dòng đơn hàng
    is_discount_item = fields.Boolean('Là sản phẩm khuyến mãi', default=False)
    line_notes = fields.Text('Ghi chú dòng')
    
    @api.onchange('is_discount_item')
    def _onchange_is_discount_item(self):
        if self.is_discount_item:
            self.price_unit = 0.0