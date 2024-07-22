from odoo import models, fields



class ProductSubSubCategory(models.Model):
    _name = 'product.subsubcategories'
    _description = 'Product SubSubCategory'

    name = fields.Char(string='Name', required=True)
    subcategory_id = fields.Many2one('product.subcategories',string="Category")
    product_lines = fields.Many2many('product.template', 'subsubcategory_id', string='Product Lines')

class ProductInherited(models.Model):
    _inherit = 'product.template'
    _description = 'Product'

    subsubcategory_id = fields.Many2many('product.subsubcategories', string='Sub-Subcategory')

