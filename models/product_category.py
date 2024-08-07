from odoo import models, fields

class ProductCategory(models.Model):
    _name = 'product.categories'
    _description = 'Product Category'

    name = fields.Char(string='Name', required=True)
    subcategories_lines = fields.One2many('product.subcategories', 'category_id', string='SubCategories')

    category_type = fields.Selection([
        ('product','Product'),
        ('service','Service')
    ],string="Request Type")




class ProductSubCategoryLines(models.Model):
    _name = 'product.subcategories.lines'

    category_id = fields.Many2one('product.categories', string='Category')
    subcategories = fields.Many2one('product.subcategories',string="SubCategories")
    
    


# class ProductTemplateInherited(models.Model):
#     _inherit = 'product.template'

#     subcategory_id = fields.Many2many('product.subcategories', string='Subcategory')