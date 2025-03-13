from odoo import models, fields, api

class ProductInventory(models.Model):
    _name = 'custom.product.inventory'
    _description = 'Custom Product Inventory View'
    
    name = fields.Char(string='Product Name')
    product_id = fields.Many2one('product.product', string='Product')
    quantity_available = fields.Float(string='Quantity Available', related='product_id.qty_available')
    list_price = fields.Float(string='Sales Price', related='product_id.list_price')
    standard_price = fields.Float(string='Cost Price', related='product_id.standard_price')
    categ_id = fields.Many2one('product.category', string='Category', related='product_id.categ_id')
    
    @api.model
    def create(self, vals):
        if 'product_id' in vals and vals.get('product_id'):
            product = self.env['product.product'].browse(vals.get('product_id'))
            vals['name'] = product.name
        return super(ProductInventory, self).create(vals)