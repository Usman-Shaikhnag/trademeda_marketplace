from odoo import models, fields, api
from datetime import timedelta, date

class RequestForQuotation(models.Model):
    _name = 'trademeda.rfq'
    _rec_name = 'rfq_no'

    
    rfq_no = fields.Char("RFQ NO",default="New")
    request_type = fields.Selection([
        ('product','Product'),
        ('service','Service')
    ],string="Request Type")

    rfq_date = fields.Date('Date')
    partner_id = fields.Many2one('res.partner',string="Customer")
    subcategory = fields.Many2one('product.subcategories',string="Subcategory")
    product_subsubcategory = fields.Many2one('product.template',string="Sub-Subcategory")
    product_name = fields.Char('Product Name')
    quantity = fields.Integer("Quantity")
    unit = fields.Many2one('uom.uom',string="Unit")
    packaging_requirements = fields.Char("Packaging Requirements")
    sample_policy = fields.Char("Sample Policy")
    target_price = fields.Float('Target Price')
    payment_terms = fields.Selection([
        ('cash_advance','Cash in Advance'),
        ('letter_of_credit','Letter of Credit'),
        ('documentary_collection','Documentary Collection'),
        ('open_account','Open Account'),
        ('advance_payment','Advance Payment'),
        ('consignment','Consignment'),
        ('cash_on_delivery','Cash on Delivery (COD)'),
        ('payment_in_installments','Payment in Installments'),
        ('bill_of_exchange','Bill of Exchange'),
        ('telegraphic_transfer','Telegraphic transfer')
    ],string="Payment Terms")
    shipping_terms = fields.Selection([
        ('fob','FOB (Free on Board)'),
        ('fca','FCA (Free Carrier)'),
        ('exw','EXW (Ex Works)'),
        ('fas','FAS (Free Alongside Ship)'),
        ('dap','DAP (Delivered at Place)'),
        ('dat','DAT (Delivered at Terminal)'),
        ('cif','CIF (Cost, Insurance and Freight)'),
        ('cip','CIP (Carriage and Insurance Paid to)'),
        ('cfr','CFR (Cost and Freight)'),
        ('ddp','DDP (Delivery Duty Paid)'),
        ('cpt','CPT (Carriage paid to)'),
    ],string="Shipping Terms")

    currency = fields.Many2one('res.currency',string="Currency")

    suppliers_country = fields.Many2one('res.country',string="Supplier from")
    destination = fields.Many2one('res.country',string="Destination")


    product_description = fields.Text("Product Description")
    contact_person_name = fields.Char("Contact Person Name")
    contact_person_designation = fields.Char("Contact Person Designation")

    company_name = fields.Char('Company Name')
    company_address = fields.Text('Company Address')
    phone_number = fields.Char("Phone Number")
    email_id = fields.Char("Email ID")
    website = fields.Char("Website")
    product_image = fields.Binary('Image')
    file_name = fields.Char("File Name")
    active = fields.Boolean(string="Active",default=True)
    state = fields.Selection([
        ('active','Active'),
        ('closed','Closed'),
        ('expired','Expired'),
        ('deleted','Deleted')
    ],string="State",default="active")
    views = fields.Integer('Views')
    # message = fields.Text('message')


    quotations = fields.One2many('rfq.quotations','rfq_id',string="Quotations")
    days_remaining = fields.Integer(string="Days Remaining",default=100,compute="calculate_days_remaining")
    end_date = fields.Date('Date',compute="calculate_end_date")

    @api.depends('create_date')
    def calculate_end_date(self):
        for record in self:
            if record.create_date:
                record.end_date = record.create_date + timedelta(days=100)
            else:
                record.end_date = False

    @api.depends('end_date')
    def calculate_days_remaining(self):
        for record in self:
            if record.end_date:
                today = date.today()
                delta = (record.end_date - today).days
                record.days_remaining = max(delta, 0)
            else:
                record.days_remaining = 0



    @api.model
    def _cron_expire_rfqs(self):
        # today = date.today()
        # expiration_date = today - timedelta(days=100)
        
        # expired_rfqs = self.search([('rfq_date', '<=', expiration_date), ('state', '=', 'active')])
        # for rfq in expired_rfqs:
        #     rfq.write({'state': 'expired'})
        today = date.today()
        expiration_date = today - timedelta(days=100)
        
        # Search for active RFQs
        rfqs = self.search([('state', '=', 'active')])

        for rfq in rfqs:
            # Calculate expiration based on create_date
            if rfq.create_date:
                expiration_threshold = rfq.create_date.date() + timedelta(days=100)
                rfq.days_remaining = (expiration_threshold - today).days
            else:
                rfq.days_remaining = 0

            # Check if RFQ should be expired
            if rfq.days_remaining <= 0:
                rfq.write({'state': 'expired'})
    



    @api.model
    def create(self, vals):
        if vals.get('rfq_no', 'New') == 'New':
            vals['rfq_no'] = self.env['ir.sequence'].next_by_code('trademeda.rfq') or 'New'
        return super(RequestForQuotation, self).create(vals)
    
class RfqQuotations(models.Model):
    _name = 'rfq.quotations'

    rfq_id = fields.Many2one('trademeda.rfq',string="RFQ ID")

    quotation_no = fields.Char("Quotation Id",default="New")
    partner_id = fields.Many2one('res.partner',string="Customer")
    company_name = fields.Char("Company Name")
    contact_name = fields.Char("Name")
    email = fields.Char("Email")
    phone = fields.Char("Phone")
    country_id = fields.Many2one('res.country',string="Country")
    message = fields.Text("Message")


    @api.model
    def create(self, vals):
        if vals.get('quotation_no', 'New') == 'New':
            vals['quotation_no'] = self.env['ir.sequence'].next_by_code('trademeda.rfq_quotation') or 'New'
        return super(RfqQuotations, self).create(vals)
