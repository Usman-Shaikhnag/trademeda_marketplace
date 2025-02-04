from odoo import models, fields, api
from datetime import timedelta, date

class TrademedaConf(models.Model):
    _name = 'trademeda.conf'

    free_subscription_days = fields.Integer("Free Subscription Days")