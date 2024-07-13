from odoo import http
from odoo.http import request
import base64
class HomepageController(http.Controller):

    @http.route('/home', auth='public', website=True)
    def home(self, **kwargs):
        product_categories = request.env['product.categories'].sudo().search([])
        vals = {"product_categories": product_categories}
        return request.render('trademeda.homepage',vals)
    


    @http.route('/signup', auth='public', website=True)
    def signup(self, **kwargs):
        # import wdb;wdb.set_trace()
        countries = request.env['res.country'].sudo().search([])
        vals = {"countries":countries}
        return request.render('trademeda.signup',vals)
    
    @http.route('/signin', auth='public', website=True)
    def signin(self, **kwargs):
        # import wdb;wdb.set_trace()
        
        return request.render('trademeda.signin')
    
    @http.route('/product', auth='public', website=True)
    def product(self, **kwargs):
        return request.render('trademeda.product_details')
    
    @http.route('/profile', auth='public', website=True)
    def UserProfile(self, **kwargs):

        user = request.env.user
        partner_id = user.partner_id
        categories = request.env['product.categories'].sudo().search([])
        subcategories = request.env['product.subcategories'].sudo().search([])
        products = request.env['product.template'].sudo().search([])
        user_products = request.env['product.customer.images'].sudo().search([('partner_id','=',partner_id.id)])

        vals = {
            'user':user,
            'partner':partner_id,
            'categories':categories,
            'subcategories':subcategories,
            'products':products,
            'user_products':user_products,
            't_product_id':1

        }
        return request.render('trademeda.user_profile',vals)
    
    @http.route(['/my/products/subcategories'], type='http', auth="user")
    def get_subcategories(self, category_id):
        subcategories = request.env['product.subcategories'].sudo().search([('category_id', '=', int(category_id))])
        subcategory_list = [{'id': subcategory.id, 'name': subcategory.name} for subcategory in subcategories]
        import wdb;wdb.set_trace()

        return {'subcategories': subcategory_list}
        
    @http.route(['/signup/createuser'], method=["POST"], type="http", auth="public", website=True)
    def CreateUser(self, **kw):
        # import wdb;wdb.set_trace()
        if request.httprequest.method == 'POST':
            # Extract form data
            name = kw.get("name")
            city = kw.get("city")
            zip_code = kw.get("zip_code")
            state = kw.get("state")
            phone = kw.get("phone_number")
            email = kw.get("email")
            password = kw.get("password")
            confirm_password = kw.get("confirm_password")

            # Basic validation
            if not all([name, city, zip_code, state, phone, email, password, confirm_password]):
                return request.redirect("/signup?error=missing_fields")

            if password != confirm_password:
                return request.redirect("/signup?error=password_mismatch")

            portal_group = request.env.ref('base.group_portal')
            # Prepare user data for creation
            user_data = {
                "login": email,
                'password': password,
                'name': name,
                'groups_id': [(6, 0, [portal_group.id])]
                # 'sel_groups_1_10_11':'[10]'
                
                # Add any additional fields if needed
            }
            
            # 'sel_groups_1_9_10':''
            try:
                # Create the user
                request.env['res.users'].sudo().create(user_data)
                request.env['res.partner'].sudo().create({
                    'name':name,
                    'membership_state':'free',
                    'free_member':True,
                    'member_type':kw.get('role')
                    # 'x_studio_member_type':
                })
                
                return request.redirect("/signin")
            except Exception as e:
                # Handle exceptions, such as email already existing
                emails = request.env['res.users'].sudo().search([])
                if(email in emails):
                    return request.redirect("/signup?error=creation_failed")
                

        return request.redirect("/signup")


    @http.route('/custom_login', type='http', auth='none', methods=['POST'], csrf=False)
    def custom_login(self, **kw):
        email = kw.get('login')
        password = kw.get('password')
        
        # Authenticate the user
        uid = request.session.authenticate(request.env.cr.dbname, email, password)

        if uid:
            user = request.env['res.users'].browse(uid)
            if user.has_group('base.group_user'):  # Internal User
                return request.redirect('/web')
            else:  # Portal/Public User
                return request.redirect('/home')
        else:
            # Authentication failed, redirect back to login with an error
            return request.redirect('/web/login?error=login_failed')
        

    @http.route('/web/login', auth='public', website=True)
    def signin_redirect(self, **kwargs):
        return request.render('trademeda.signin')
    
    @http.route('/profile/updateuser', auth='public', website=True)
    def update_profile(self, **kwargs):
        # import wdb;wdb.set_trace()

        return request.render('trademeda.user_profile')
    

    @http.route(['/profile/updateuser'], method=["POST"], type="http", auth="public", website=True)
    def UpdateUser(self, **kw):
        # import wdb;wdb.set_trace()
        user = request.env.user
        partner_id = user.partner_id
        if request.httprequest.method == 'POST':
            # Extract form data
            name = kw.get("name")
            city = kw.get("city")
            zip_code = kw.get("zip_code")
            state = kw.get("state")
            phone = kw.get("phone_number")
            email = kw.get("email")

            partner_id.sudo().write({
                'phone':phone,
                'city':city,
                'zip':zip_code,
                'state_id':state,
                'email':email
                

            })
            return request.redirect("/profile")



    @http.route('/profile/supplier', auth='public', website=True)
    def supplier_profile(self, **kwargs):
        # import wdb;wdb.set_trace()
        user = request.env.user
        partner_id = user.partner_id
        products = request.env['product.customer.images'].sudo().search([('partner_id','=',7)])

        vals = {
            "products": products,
            'partner':partner_id
            }


        return request.render('trademeda.supplier_profile',vals)
    

    @http.route(['/profile/updatedocuments'], method=["POST"], type="http", auth="user", website=True)
    def UpdateDocuments(self, **kw):
        # import wdb;wdb.set_trace()
        user = request.env.user
        partner_id = user.partner_id
        if request.httprequest.method == 'POST':
            # Extract form data
            company_registration = kw.get("company_registration").read()
            company_registration_name = kw.get("company_registration_name")

            company_address_proof = kw.get("company_address_proof").read()
            company_address_proof_name = kw.get("company_address_proof_name")

            trading_license = kw.get("trading_license").read()
            trading_license_name = kw.get("trading_license_name")

            identity_proof = kw.get("identity_proof").read()
            identity_proof_name = kw.get("identity_proof_name")

            prior_import_export = kw.get("prior_import_export").read()
            prior_import_export_name = kw.get("prior_import_export_name")

            tax_id_proof = kw.get("tax_id_proof").read()
            tax_id_proof_name = kw.get("tax_id_proof_name")

            if company_registration:
                partner_id.sudo().write({
                    'company_registration':base64.b64encode(company_registration),
                    'company_registration_name':company_registration_name,
                })

            if company_address_proof:
                partner_id.sudo().write({
                    'company_address_proof':base64.b64encode(company_address_proof),
                    'company_address_proof_name':company_address_proof_name,
                })

            if trading_license:
                partner_id.sudo().write({
                    'trading_license':base64.b64encode(trading_license),
                    'trading_license_name':trading_license_name,
                })
            
            if identity_proof:
                partner_id.sudo().write({
                    'identity_proof':base64.b64encode(identity_proof),
                    'identity_proof_name':identity_proof_name,
                })

            if prior_import_export:
                partner_id.sudo().write({
                    'prior_import_export':base64.b64encode(prior_import_export),
                    'prior_import_export_name':prior_import_export_name,
                })

            if tax_id_proof:
                partner_id.sudo().write({
                    'tax_id_proof':base64.b64encode(tax_id_proof),
                    'tax_id_proof_name':tax_id_proof_name
                })

            return request.redirect("/profile")
        

    @http.route(['/profile/addproduct'], method=["POST"], type="http", auth="user", website=True)
    def addProducts(self, **kw):
        # import wdb;wdb.set_trace()
        user = request.env.user
        partner_id = user.partner_id
        if request.httprequest.method == 'POST':
            # Extract form data
            product_image = kw.get('upload_product').read()
            product_description = kw.get('product_description')

            if product_image:
                partner_id.product_images.sudo().create({
                    'partner_id': partner_id.id,
                    'product_image':base64.b64encode(product_image),
                    'product_description':product_description
                })

            return request.redirect("/profile")