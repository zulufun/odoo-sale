# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request

class CustomProductInventory(http.Controller):
    @http.route(['/custom_sale/products'], type='http', auth="user", website=True)
    def product_inventory(self, **kw):
        products = request.env['custom.product.inventory'].sudo().search([])
        values = {
            'products': products,
        }
        return request.render('custom_sale.product_inventory_page', values)