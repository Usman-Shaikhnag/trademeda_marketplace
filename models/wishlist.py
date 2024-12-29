from odoo import models, fields

class Wishlist(models.Model):
    _name = 'user.wishlist'
    _description = 'Wishlist'

    partner_id = fields.Many2one('res.partner',string="Customer")
    product_id = fields.Many2one('product.customer.images',string="Product")