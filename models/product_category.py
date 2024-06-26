from odoo import models, fields

class ProductCategory(models.Model):
    _name = 'product.categories'
    _description = 'Product Category'

    name = fields.Char(string='Name', required=True)
    product_lines = fields.One2many('product.lines', 'category_id', string='Product Lines')

class ProductLines(models.Model):
    _name = 'product.lines'
    _description = 'Product Lines'

    category_id = fields.Many2one('product.categories', string='Category')
    product_id = fields.Many2one('product.template', string='Product')