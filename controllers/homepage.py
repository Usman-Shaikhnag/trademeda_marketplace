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
        
        return request.render('trademeda.signup')
    
    @http.route('/signin', auth='public', website=True)
    def signin(self, **kwargs):
        # import wdb;wdb.set_trace()
        
        return request.render('trademeda.signin')
    
    @http.route('/product', auth='public', website=True)
    def product(self, **kwargs):
        return request.render('trademeda.product_details')
        
    @http.route(['/signup/createuser'],method=["POST"], type="http", auth="public", website=True)
    def CreateUser(self, **kw):

        import wdb; wdb.set_trace();
        
        if request.httprequest.method == 'POST':
            name = kw.get("name")
            city = kw.get("city")
            zip_code = kw.get("zip")
            state_id = kw.get("state_id")
            phone = kw.get("phone")
            mobile = kw.get("mobile")
            email = kw.get("email")
            password = kw.get("password")

            
            user_data = {
                "login":email,
                'password':password
            }
            
            
            request.env['res.users'].sudo().create(user_data)
            
            return request.redirect("/signin")
