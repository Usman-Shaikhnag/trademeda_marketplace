from odoo import models, fields

class ProductCategory(models.Model):
    _name = 'product.categories'
    _description = 'Product Category'

    name = fields.Char(string='Name', required=True)
    subcategories_lines = fields.One2many('product.subcategories.lines', 'category_id', string='SubCategories')

class ProductSubCategory(models.Model):
    _name = 'product.subcategories'
    _description = 'Product SubCategory'

    name = fields.Char(string='Name', required=True)
    product_lines = fields.Many2many('product.lines', 'subcategory_id', string='Product Lines')

class ProductLines(models.Model):
    _name = 'product.lines'
    _description = 'Product Lines'

    subcategory_id = fields.Many2one('product.subcategories', string='Subcategory')
    product_id = fields.Many2one('product.template', string='Product')

class ProductSubCategoryLines(models.Model):
    _name = 'product.subcategories.lines'

    category_id = fields.Many2one('product.categories', string='Category')
    subcategories = fields.Many2one('product.subcategories',string="SubCategories")
    
    



