from odoo import models, fields



class ProductSubCategory(models.Model):
    _name = 'product.subcategories'
    _description = 'Product SubCategory'

    name = fields.Char(string='Name', required=True)
    category_id = fields.Many2one('product.categories',string="Category")
    subsubcategories_lines = fields.One2many('product.template', 'subcategory_id', string='Sub-Subcategories')

    ranking = fields.Integer("Ranking")
    points = fields.Integer("Points")
    icon = fields.Binary('Icon')
    icon_name = fields.Char("Icon Name")


    def action_calculate_ranking(self):
        # Fetch all subcategories
        subcategories = self.env['product.subcategories'].sudo().search([])

        # Sort the subcategories based on points in descending order
        sorted_subcategories = subcategories.sorted(key=lambda sub: sub.points, reverse=True)

        # Assign rankings based on sorted order
        ranking = 1
        for subcategory in sorted_subcategories:
            subcategory.sudo().write({
                'ranking': ranking,
            })
            ranking += 1