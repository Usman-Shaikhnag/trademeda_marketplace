from odoo import models, fields



class ProductSubCategory(models.Model):
    _name = 'product.subcategories'
    _description = 'Product SubCategory'

    name = fields.Char(string='Name', required=True)
    category = fields.Many2one('product.categories',string="Category")
    product_lines = fields.One2many('product.lines', 'subcategory_id', string='Product Lines')

class ProductLines(models.Model):
    _name = 'product.lines'
    _description = 'Product Lines'

    subcategory_id = fields.Many2one('product.subcategories', string='Subcategory')
    product_id = fields.Many2one('product.template', string='Product')

