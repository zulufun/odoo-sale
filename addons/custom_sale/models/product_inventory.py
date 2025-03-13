# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ProductInventory(models.Model):
    _name = 'custom.product.inventory'
    _description = 'Custom Product Inventory View'
    _order = 'product_id'
    _auto = False

    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', readonly=True)
    product_name = fields.Char(string='Product Name', readonly=True)
    qty_available = fields.Float(string='Quantity On Hand', readonly=True)
    virtual_available = fields.Float(string='Forecasted Quantity', readonly=True)
    incoming_qty = fields.Float(string='Incoming', readonly=True)
    outgoing_qty = fields.Float(string='Outgoing', readonly=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', readonly=True)
    categ_id = fields.Many2one('product.category', string='Product Category', readonly=True)
    list_price = fields.Float(string='Sales Price', readonly=True)
    standard_price = fields.Float(string='Cost', readonly=True)

    def init(self):
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW custom_product_inventory AS (
                SELECT
                    p.id,
                    p.id as product_id,
                    pt.id as product_tmpl_id,
                    pt.name as product_name,
                    p.qty_available,
                    p.virtual_available,
                    p.incoming_qty,
                    p.outgoing_qty,
                    pt.uom_id,
                    pt.categ_id,
                    pt.list_price,
                    p.standard_price
                FROM
                    product_product p
                    JOIN product_template pt ON (p.product_tmpl_id = pt.id)
                WHERE
                    pt.sale_ok = true AND pt.active = true
            )
        """)