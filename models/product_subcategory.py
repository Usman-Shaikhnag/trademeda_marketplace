from odoo import models, fields



class ProductSubCategory(models.Model):
    _name = 'product.subcategories'
    _description = 'Product SubCategory'

    name = fields.Char(string='Name', required=True)
    category_id = fields.Many2one('product.categories',string="Category")
    subsubcategories_lines = fields.One2many('product.subsubcategories', 'subcategory_id', string='Sub-Subcategories')
