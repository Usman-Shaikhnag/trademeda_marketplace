from odoo import models, fields

class MissionVision(models.Model):
    _name = 'trademeda.mission'
    _description = 'FAQ'

    mission_img = fields.Binary('Mission and Vision')
    img_name = fields.Char('filename')

    