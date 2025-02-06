from odoo import models, fields, api
from datetime import timedelta, date

class TrademedaConf(models.Model):
    _name = 'trademeda.conf'

    free_subscription_days = fields.Integer("Free Subscription Days")
    contact_email = fields.Char("Contact Us Email")
    contact_phone = fields.Char("Contact Us Phone")
    contact_text = fields.Text("Contact Us Text")

