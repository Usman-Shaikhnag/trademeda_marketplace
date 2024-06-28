from odoo import http
from odoo.http import request

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
        return request.render('trademeda.user_profile')
        
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
    def product(self, **kwargs):
        return request.render('trademeda.signin')