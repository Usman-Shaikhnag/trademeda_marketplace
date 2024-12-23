from odoo import models, fields, api

class TrademedaEmail(models.Model):
    _name = 'trademeda.email'
    _description = 'Emails'

    member_type = fields.Selection([
        ('buyer','Buyer'),
        ('seller','Seller'),
        ('both','Both')
    ],string="Member Type")

    subcategory = fields.Many2one('product.subcategories',string="Subcategory")
    subject = fields.Char("Subject")
    message = fields.Text('Message')


    @api.depends('message','subcategory','member_type','subject')
    def sendMail(self):
        for record in self:
            emails = []
            if record.member_type == 'seller':
                sellers = record.env['product.customer.images'].sudo().search([('product_id.subcategory_id.id','=',record.subcategory.id)])
                for seller in sellers:
                    email = seller.partner_id.email
                    emails.append(email)
            elif record.member_type == 'buyer':
                buyers = record.env['trademeda.rfq'].sudo().search([('subcategory','=',record.subcategory.id)])
                for buyer in buyers:
                    email = buyer.partner_id.email
                    emails.append(email)

            else:
                sellers = record.env['product.customer.images'].sudo().search([('product_id.subcategory_id.id','=',record.subcategory.id)])
                for seller in sellers:
                    email = seller.partner_id.email
                    emails.append(email)
                buyers = record.env['trademeda.rfq'].sudo().search([('subcategory','=',record.subcategory.id)])
                for buyer in buyers:
                    email = buyer.partner_id.email
                    emails.append(email)
            for email in emails:
                mail = self.env['mail.mail'].sudo().create({
                    'subject': record.subject,
                    'body_html': record.message,
                    'email_to': email,
                    'email_from': 'info@trademeda.com',
                })
                mail.send()
