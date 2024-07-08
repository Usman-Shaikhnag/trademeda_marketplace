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
        vals = {
            'user':user,
            'partner':partner_id
        }
        return request.render('trademeda.user_profile',vals)
        
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



            # try:
            # # Get file data from request
            #     company_registration_file = kw.get('company_registration').read() if 'company_registration' in kw else False
            #     company_address_proof_file = kw.get('company_address_proof').read() if 'company_address_proof' in kw else False
            #     identity_proof_file = kw.get('identity_proof').read() if 'identity_proof' in kw else False
            #     trading_license_file = kw.get('trading_license').read() if 'trading_license' in kw else False
            #     other_documents_file = kw.get('other_documents').read() if 'other_documents' in kw else False
            #     prior_import_export_file = kw.get('prior_import_export').read() if 'prior_import_export' in kw else False
            #     tax_id_proof_file = kw.get('tax_id_proof').read() if 'tax_id_proof' in kw else False
                
            #     # Convert file content to base64 (optional)
            #     def convert_to_base64(file_data):
            #         if file_data:
            #             return base64.b64encode(file_data)
            #         return False
                
            #     # Write to partner record
            #     partner_id.sudo().write({
            #         'x_studio_company_registration': convert_to_base64(company_registration_file),
            #         'x_studio_company_address_proof': convert_to_base64(company_address_proof_file),
            #         'x_studio_identity_proof': convert_to_base64(identity_proof_file),
            #         'x_studio_trading_license': convert_to_base64(trading_license_file),
            #         'x_studio_other_documents': convert_to_base64(other_documents_file),
            #         'x_studio_proof_of_prior_import_export': convert_to_base64(prior_import_export_file),
            #         'x_studio_tax_id_proof': convert_to_base64(tax_id_proof_file),
            #     })

            #     return request.redirect("/profile")

            # except Exception as e:
            #     # Handle exception (e.g., file read error, database update error)
            #     return request.redirect("/signup?error=upload_failed")

            # return request.redirect("/signup")

    @http.route('/profile/supplier', auth='public', website=True)
    def update_profile(self, **kwargs):
        # import wdb;wdb.set_trace()

        return request.render('trademeda.supplier_profile')