from odoo import models, fields, api

class CustomerTestimony(models.Model):
    _name = 'customer.testimony'
  

    partner_id = fields.Many2one('res.partner',string="Customer")
    rating = fields.Integer("Rating")
    testimony = fields.Text("testimony")
    display = fields.Boolean('Display on Homepage')