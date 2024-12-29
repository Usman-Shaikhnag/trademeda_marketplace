from odoo import models, fields


class ContactUs(models.Model):
    _name = 'trademada.contact.us'

    user_name = fields.Char("Name")
    message = fields.Text(string="Message")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    product = fields.Char("Product")
    country = fields.Many2one('res.country', string="Country")
    

