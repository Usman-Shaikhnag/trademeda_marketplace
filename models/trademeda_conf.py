from odoo import models, fields, api
from datetime import timedelta, date

class TrademedaConf(models.Model):
    _name = 'trademeda.conf'

    free_subscription_days = fields.Integer("Free Subscription Days")
    # contact_email = fields.Char("Contact Us Email")
    # contact_phone = fields.Char("Contact Us Phone")
    # contact_text = fields.Text("Contact Us Text")

    contactus_image = fields.Binary("Contact Us Image")
    contactus_imagename = fields.Char("Contact Us Image name")

    brochure_file = fields.Binary("Brochure")
    brochure_filename = fields.Char("Brochure Filename")
    


