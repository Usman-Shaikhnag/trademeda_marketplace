from odoo import models, fields

class RequestForQuotation(models.Model):
    _name = 'trademeda.rfq'

    
    rfq_no = fields.Char("RFQ NO")
    request_type = fields.Selection([
        ('product','Product'),
        ('service','Service')
    ],string="Request Type")

    rfq_date = fields.Date('Date')
    product_name = fields.Many2one('product.template',string="Product")
    partner_id = fields.Many2one('res.partner',string="Customer")

    quantity = fields.Integer("Quantity")
    unit = fields.Many2one('uom.uom',string="Unit")
    packaging_requirements = fields.Char("Packaging Requirements")
    sample_policy = fields.Char("Sample Policy")
    target_price = fields.Float('Target Price')
    payment_terms = fields.Char("Payment Terms")
    shipping_terms = fields.Selection([
        ('fob','FOB (Free on Board)'),
        ('fca','FCA (Free Carrier)'),
        ('exw','EXW (Ex Works)'),
        ('fas','FAS (Free Alongside Ship)'),
        ('dap',' DAP (Delivered at Place)'),
        ('dat','DAT (Delivered at Terminal)'),
        ('cif','CIF (Cost, Insurance and Freight)'),
        ('cip','CIP (Carriage and Insurance Paid to)'),
        ('cfr','CFR (Cost and Freight)'),
        ('ddp','DDP (Delivery Duty Paid)'),
        ('cpt','CPT (Carriage paid to)'),
    ],string="Shipping Terms")

    product_description = fields.Text("Product Description")
    contact_person_name = fields.Char("Contact Person Name")
    contact_person_designation = fields.Char("Contact Person Designation")

    company_name = fields.Char('Company Name')
    company_address = fields.Text('Company Address')
    phone_number = fields.Char("Phone Number")
    email_id = fields.Char("Email ID")
    website = fields.Char("Website")
    



