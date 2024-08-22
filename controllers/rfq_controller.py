from odoo import http
from odoo.http import request
import base64
import json

class RFQController(http.Controller):

    @http.route('/post_rfq_page', auth='user', website=True)
    def rfqPage(self, **kwargs):
        vals = {
            'logged_in':request.env.user != request.env.ref('base.public_user')
        }
        return request.render('trademeda.rfq_page',vals)
    
    @http.route('/rfq/fetchCategories/<int:request_type>', auth='user', website=True)
    def getCategories(self, request_type , **kwargs):
        categories = request.env['product.subcategories'].sudo().search([('category_type','=',request_type)])
        category_list = [{
            'id': category.id,
            'name': category.name,
        } for category in categories]
        return json.dumps(category_list)
    
    @http.route('/view_rfq/<int:rfqId>', auth='user', website=True)
    def viewrfqPage(self,rfqId, **kwargs):
        rfq = request.env['trademeda.rfq'].sudo().search([('id','=',rfqId)])
        vals = {
            'rfq':rfq,
            'logged_in':request.env.user != request.env.ref('base.public_user')
        }
        return request.render('trademeda.view_quotation',vals)
    
    @http.route('/send_enquiry/<int:rfqId>',method=['POST'],type='json', auth='user', website=True)
    def sendEnquiry(self,rfqId, **kwargs):
        # import wdb;wdb.set_trace()
        user = request.env.user
        partner_id = user.partner_id

        rfq = request.env['trademeda.rfq'].sudo().search([('id','=',rfqId)])
        body = request.httprequest.get_json()
        if body['country'] != '':
            country = request.env['res.country'].sudo().search([('id','=',int(body['country']))]).id
        else:
            country = False
        rfq.quotations.sudo().create({
            'rfq_id':rfqId,
            'partner_id':partner_id.id,
            'company_name':body['company_name'],
            'contact_name':body['name'],
            'email':body['email'],
            'phone':body['phone'],
            'country_id':country,
            'message':body['message']

        })

        return json.dumps({'status':'ok'})


    