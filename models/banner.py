from odoo import models, fields

class Banners(models.Model):
    _name = 'trademeda.banners'
    _description = 'Banners'

    # banners = fields.One2many('trademeda.banners.line','banner_id')
    banner_image = fields.Binary('Banner Image')
    image_name = fields.Char('Image Name')
    partner_id = fields.Many2one('res.partner',string="Customer")
    slide_no = fields.Integer('Slide No')