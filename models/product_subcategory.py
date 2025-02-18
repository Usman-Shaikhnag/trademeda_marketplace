from odoo import models, fields,api



class ProductSubCategory(models.Model):
    _name = 'product.subcategories'
    _description = 'Product SubCategory'

    name = fields.Char(string='Name', required=True)
    category_id = fields.Many2one('product.categories',string="Category")
    subsubcategories_lines = fields.One2many('product.template', 'subcategory_id', string='Sub-Subcategories')

    ranking = fields.Integer("Ranking")
    points = fields.Integer("Daily Points")
    total_points = fields.Integer("Total Points",compute="_compute_total_daily_points")
    icon = fields.Binary('Icon')
    icon_name = fields.Char("Icon Name")

    daily_points = fields.One2many('subcategory.daily.points', 'subcategory_id', string='Subcategories Daily Points')
    # total_points = fields.Integer("Total Points Daily",compute="_compute_total_daily_points")


    def action_calculate_ranking(self):
        # Fetch all subcategories
        subcategories = self.env['product.subcategories'].sudo().search([])

        # Sort the subcategories based on points in descending order
        sorted_subcategories = subcategories.sorted(key=lambda sub: sub.total_points, reverse=True)

        # Assign rankings based on sorted order
        ranking = 1
        for subcategory in sorted_subcategories:
            subcategory.sudo().write({
                'ranking': ranking,
            })
            ranking += 1

    @api.depends('daily_points')
    def _compute_total_daily_points(self):
        total = 0
        for point in self.daily_points:
            total = total + point.points
        self.total_points = total

    def action_points_update(self):
        subcategories = self.env['product.subcategories'].sudo().search([])

        # import wdb;wdb.set_trace()
        for subcategory in subcategories:

            if len(subcategory.daily_points) >= 21:
                oldest_record = subcategory.daily_points.sorted('create_date')[0]
                oldest_record.unlink()

            # Create a new daily points record
            self.env['subcategory.daily.points'].create({
                'points': subcategory.points,  
                'subcategory_id': subcategory.id,  
            })

            # Reset points after storing the day's total
            subcategory.write({'points': 0})

class SubCategoryDailyPoints(models.Model):
    _name = 'subcategory.daily.points'

    subcategory_id = fields.Many2one('product.subcategories',string="Subcategory Id")
    points = fields.Integer("Points")
    create_date = fields.Datetime("Created On", default=fields.Datetime.now)