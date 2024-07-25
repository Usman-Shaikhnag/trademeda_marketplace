from odoo import models, fields

class CountryInherited(models.Model):
    _inherit = 'res.country'

    continent = fields.Selection([
        ('asia','Asia'),
        ('europe','Europe'),
        ('north_america','North America'),
        ('south_america','South America'),
        ('africa','Africa'),
        ('oceania','Oceania'),
        ('antarctica','Antarctita'),
    ],string="Continent")