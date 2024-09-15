from odoo import models, fields

class Faqs(models.Model):
    _name = 'trademeda.faqs'
    _description = 'FAQ'

    question = fields.Char("Question")
    answer = fields.Text("Answer")