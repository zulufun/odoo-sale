from odoo import models, fields, tools

class SaleReport(models.Model):
    _name = 'custom.sale.report'
    _description = 'Báo cáo bán hàng'
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'
    
    date = fields.Datetime(string='Ngày đặt hàng', readonly=True)
    order_id = fields.Many2one('custom.sale.order', string='Đơn hàng', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Khách hàng', readonly=True)
    product_id = fields.Many2one('product.product', string='Sản phẩm', readonly=True)
    company_id = fields.Many2one('res.company', string='Công ty', readonly=True)
    user_id = fields.Many2one('res.users', string='Nhân viên bán hàng', readonly=True)
    price_subtotal = fields.Float(string='Thành tiền', readonly=True)
    price_total = fields.Float(string='Tổng cộng', readonly=True)
    price_tax = fields.Float(string='Thuế', readonly=True)
    state = fields.Selection([
        ('draft', 'Bản thảo'),
        ('sent', 'Đã gửi'),
        ('sale', 'Đơn hàng bán'),
        ('done', 'Hoàn thành'),
        ('cancel', 'Hủy bỏ'),
    ], string='Trạng thái', readonly=True)
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''
            CREATE or REPLACE VIEW %s as (
                SELECT
                    row_number() OVER () as id,
                    l.create_date as date,
                    l.order_id as order_id,
                    l.product_id as product_id,
                    l.price_subtotal as price_subtotal,
                    l.price_total as price_total,
                    l.price_tax as price_tax,
                    s.partner_id as partner_id,
                    s.user_id as user_id,
                    s.company_id as company_id,
                    s.state as state
                FROM custom_sale_order_line l
                JOIN custom_sale_order s ON (l.order_id = s.id)
            )
        ''' % (self._table,))
