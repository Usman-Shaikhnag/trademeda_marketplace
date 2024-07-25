from odoo import http
from odoo.http import request
import base64

class RFQController(http.Controller):

    @http.route('/post_rfq_page', auth='user', website=True)
    def rfqPage(self, **kwargs):
        return request.render('trademeda.rfq_page')