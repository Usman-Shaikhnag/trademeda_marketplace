from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import imghdr

class Banners(models.Model):
    _name = 'trademeda.banners'
    _description = 'Banners'

    # banners = fields.One2many('trademeda.banners.line','banner_id')
    banner_image = fields.Binary('Banner Image')
    image_name = fields.Char('Image Name')
    partner_id = fields.Many2one('res.partner',string="Customer")
    slide_no = fields.Integer('Slide No')


    @api.model
    def create(self, vals):
        # Check the number of existing records
        banner_count = self.env['trademeda.banners'].search_count([])
        if banner_count >= 30:
            raise ValidationError("You cannot create more than 30 banner records.")
        
        # If the limit has not been reached, proceed with the creation
        return super(Banners, self).create(vals)
    
    def get_image_src(self):
        # import wdb;wdb.set_trace()
        if self.banner_image:
            try:
                image_data = base64.b64decode(self.banner_image)
                image_format = imghdr.what(None, h=image_data)
                if image_format in ['png', 'jpeg', 'jpg','webp']:
                    return 'data:image/{};base64,{}'.format(image_format, self.banner_image.decode('utf-8'))
            except Exception as e:
                # Handle the exception if needed, e.g., logging or return None
                return None
        return None