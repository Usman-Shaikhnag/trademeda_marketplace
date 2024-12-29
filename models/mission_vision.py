from odoo import models, fields

class MissionVision(models.Model):
    _name = 'trademeda.mission'
    _description = 'FAQ'

    mission_img = fields.Binary('Mission and Vision')
    img_name = fields.Char('filename')

    def get_image_src(self):
        # import wdb;wdb.set_trace()
        if self.mission_img:
            try:
                image_data = base64.b64decode(self.mission_img)
                image_format = imghdr.what(None, h=image_data)
                if image_format in ['png', 'jpeg', 'jpg','webp']:
                    return 'data:image/{};base64,{}'.format(image_format, self.mission_img.decode('utf-8'))
            except Exception as e:
                # Handle the exception if needed, e.g., logging or return None
                return None
        return None