from odoo import models, fields

class BannerPrices(models.Model):
    _name = 'banner.pricelists'
    _description = 'Banner Pricelist'

    name = fields.Char("Name")
    price = fields.Char("Price")
    features = fields.One2many('banner.pricelist.features','pricelist_id',string="Features")
    suggested = fields.Boolean("Suggested Plan")



class BannerPricesFeatures(models.Model):
    _name = 'banner.pricelist.features'
    _description = 'Pricelist Features'

    pricelist_id = fields.Many2one('banner.pricelists')
    name = fields.Char("Name")





class MembershipPrices(models.Model):
    _name = 'membership.pricelists'
    _description = 'Banner Pricelist'

    name = fields.Char("Name")
    price = fields.Char("Price")
    duration = fields.Integer("Duration")
    duration_type = fields.Selection([
        ('months','Months'),
        ('days','Days'),
    ],string="Duration Type",default="months")

    features = fields.One2many('membership.pricelist.features','pricelist_id',string="Features")
    suggested = fields.Boolean("Suggested Plan")

class MembershipPricesFeatures(models.Model):
    _name = 'membership.pricelist.features'
    _description = 'Pricelist Features'

    pricelist_id = fields.Many2one('membership.pricelists')
    name = fields.Char("Name")
