from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    
    
    product_images = fields.One2many('product.customer.images', 'partner_id', string='Product Images')

    awards = fields.One2many('customer.awards', 'partner_id', string='Awards')
    certificates = fields.One2many('customer.certificates', 'partner_id', string='Certificates')
    customer_employees = fields.One2many('customer.employees','partner_id',string="Employees")

    member_type = fields.Selection([
        ('buyer','Buyer'),
        ('seller','Seller'),
        ('both','Both')
    ],string="Member Type")

    gender = fields.Selection([
        ('male','Male'),
        ('female','Female'),
    ],string="Gender")

    supplier_products = fields.Text("Supplier Proucts")
    buyer_products = fields.Text("Buyer Proucts")
    trader_products = fields.Text("Trader Proucts")

    primary_business = fields.Selection([
        ('buying_agent','Buying Agent'),
        ('dealer_reseller','Dealer / Reseller'),
        ('distributor','Distributor'),
        ('exporter','Exporter'),
        ('importer','Importer'),
        ('manufacturer','Manufacturer'),
        ('not_known','Not Known'),
        ('retailer','Retailer'),
        ('service_provider','Service Provider'),
        ('trader','Trader')
    ],string="Primary Business")

    establishment_year = fields.Integer("Establishment Year")
    annual_sales = fields.Selection([
        ('less_than_1000','Less than 1000 USD'),
        ('less_than_1000','Less than 10000 USD'),
        ('less_than_1000000','Less than 1000000 USD'),
        ('more_than_1000000','More than 1000000 USD'),
    ],string="Annual Sales in USD")

    no_of_employees = fields.Selection([
        ('less_than_10','Less than 10'),
        ('less_than_100','Less than 100'),
        ('less_than_1000','Less than 1000'),
        ('more_than_1000','More than 1000'),
        
    ])
    company_address = fields.Text("Company Address")
    area_code = fields.Char("Area Code")
    company_email = fields.Char("Company Email")

    company_details = fields.Text("Company Details")
    contact_person_name = fields.Char("Contact Person Name")

    company_registration = fields.Binary(string="Company Registration")
    company_registration_name = fields.Char(string="Company Registration Name")

    company_address_proof = fields.Binary(string="Company Address Proof")
    company_address_proof_name = fields.Char(string="Company Address Proof Name")

    identity_proof = fields.Binary(string="Identity Proof")
    identity_proof_name = fields.Char(string="Identity Proof Name")

    trading_license = fields.Binary(string="Trading License")
    trading_license_name = fields.Char(string="Trading License Name")

    prior_import_export = fields.Binary(string="Prior Import / Export")
    prior_import_export_name = fields.Char(string="Prior Import / Export Name")

    tax_id_proof = fields.Binary(string="Tax Id Proof")
    tax_id_proof_name = fields.Char(string="Tax Id Proof Name")


    news_title = fields.Char("News Title")
    news_image1 = fields.Binary('News Image1')
    news_image2 = fields.Binary('News Image2')
    news_image3 = fields.Binary('News Image3')
    news_image4 = fields.Binary('News Image4')
    news_image5 = fields.Binary('News Image5')

    news_image_name1 = fields.Char("Image Name1")
    news_image_name2 = fields.Char("Image Name2")
    news_image_name3 = fields.Char("Image Name3")
    news_image_name4 = fields.Char("Image Name4")
    news_image_name5 = fields.Char("Image Name5")

    news_text = fields.Text("News")





class ProductCustomerImages(models.Model):
    _name = "product.customer.images"
    _description = "Customer Product Images"

    partner_id = fields.Many2one('res.partner', string="Customer")
    product_id = fields.Many2one('product.template', string="Product")
    product_variety_name = fields.Char("Product Variety")
    product_description  = fields.Text("Product Description")
    product_image = fields.Binary('Image')
    image_name = fields.Char("Image Name")  

    product_quantity = fields.Integer("Quantity")
    packaging_requirement = fields.Char("Packaging Requirements")
    delivery_days = fields.Integer("Delivery in Days")
    product_price_usd = fields.Float("Price (in USD)")
    payment_mode = fields.Char("Payment Mode")
    sample_policy = fields.Char("Sample Policy")
    upload_date = fields.Datetime("Upload Date")


class CustomerAwards(models.Model):
    _name = "customer.awards"
    _description = "Customer Awards"

    partner_id = fields.Many2one('res.partner', string="Customer")

    award_name  = fields.Char("Award Name")
    award_description  = fields.Text("Award Description")
    award_attachment = fields.Binary('Award')
    file_name = fields.Char("File Name") 
    public_display = fields.Boolean("Public Display")


class CustomerCertificates(models.Model):
    _name = "customer.certificates"
    _description = "Customer Certificates"

    partner_id = fields.Many2one('res.partner', string="Customer")

    certificate_name  = fields.Char("Certificate Name")
    certificate_description  = fields.Text("Certificate Description")
    certificate_attachment = fields.Binary('Certificate')
    file_name = fields.Char("File Name") 
    public_display = fields.Boolean("Public Display")


class CustomerEmployees(models.Model):
    _name = "customer.employees"
    _description = "Customer Employees"

    partner_id = fields.Many2one('res.partner', string="Customer")

    employee_name  = fields.Char("Employee Name")
    employee_designation  = fields.Char("Employee Designation")
    employee_contact  = fields.Char("Employee Contact")
    employee_email  = fields.Char("Employee Email")

