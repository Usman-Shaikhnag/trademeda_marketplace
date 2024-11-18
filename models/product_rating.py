from odoo import models, fields, api

class CustomerRating(models.Model):
    _name = 'customer.rating'
  

    partner_id = fields.Many2one('res.partner',string="Customer")
    seller_id = fields.Many2one('res.partner',string="Seller")
    rating = fields.Integer("Rating")
    review = fields.Text("Review")