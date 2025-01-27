from odoo import models, fields
from odoo.exceptions import ValidationError
import base64
import imghdr

class Brochure(models.Model):
    _name = 'trademeda.brochure'
    _description = 'FAQ'

    brochure_image = fields.Binary('Brochure Image')
    image_name = fields.Char('Image Name')
    sequence = fields.Integer('Sequence')
    

    def get_image_src(self):
        # import wdb;wdb.set_trace()
        if self.brochure_image:
            try:
                image_data = base64.b64decode(self.brochure_image)
                image_format = imghdr.what(None, h=image_data)
                if image_format in ['png', 'jpeg', 'jpg','webp']:
                    return 'data:image/{};base64,{}'.format(image_format, self.brochure_image.decode('utf-8'))
            except Exception as e:
                # Handle the exception if needed, e.g., logging or return None
                return None
        return None
    
class AboutUs(models.Model):
    _name = 'trademeda.aboutus'
    _description = 'FAQ'

    aboutus_image = fields.Binary('Brochure Image')
    image_name = fields.Char('Image Name')
    sequence = fields.Integer('Sequence')
    

    def get_image_src(self):
        # import wdb;wdb.set_trace()
        if self.aboutus_image:
            try:
                image_data = base64.b64decode(self.aboutus_image)
                image_format = imghdr.what(None, h=image_data)
                if image_format in ['png', 'jpeg', 'jpg','webp']:
                    return 'data:image/{};base64,{}'.format(image_format, self.aboutus_image.decode('utf-8'))
            except Exception as e:
                # Handle the exception if needed, e.g., logging or return None
                return None
        return None