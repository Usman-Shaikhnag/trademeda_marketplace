from odoo import http
from odoo.http import request
import base64
import json
import io
import xlsxwriter
from io import BytesIO
class ProductController(http.Controller):

    @http.route(['/add-to-wishlist/<int:product_id>'], type="http", auth="user", website=True)
    def AddToWishlist(self, product_id, **kwargs):
        user = request.env.user
        partner_id = user.partner_id
        customer_product = request.env['product.customer.images'].sudo().browse(product_id)
        
        if customer_product.exists():
            # Check if the product is already in the wishlist
            existing_wishlist_item = request.env['user.wishlist'].sudo().search([
                ('partner_id', '=', partner_id.id),
                ('product_id', '=', customer_product.id)
            ], limit=1)
            
            if not existing_wishlist_item:
                # If not in wishlist, create a new entry
                request.env['user.wishlist'].sudo().create({
                    'partner_id': partner_id.id,
                    'product_id': customer_product.id
                })
        
        return request.render('trademeda.wishlist_page')
    

    @http.route(['/addToWishlistDatabase'], methods=["POST"], type="json", auth="public", website=True)
    def AddToWishlistDatabase(self, **kw):
        user = request.env.user
        partner_id = user.partner_id
        import wdb;wdb.set_trace()
        data = request.httprequest.get_json()
        
        
        
        return request.render('trademeda.wishlist_page')
       
        
    

    @http.route(['/wishlist',], type="http", auth="public", website=True)
    def GoToWishlist(self, **kwargs):
        user = request.env.user
        partner_id = user.partner_id
        # import wdb;wdb.set_trace()

        
        wishlists = request.env['user.wishlist'].sudo().search([('partner_id', '=', partner_id.id)])
        product_ids = [wishlist.product_id.id for wishlist in wishlists]
        
        actual_products = request.env['product.customer.images'].sudo().search([('id', 'in', product_ids)])
        
        vals = {
            'products': actual_products
        }

        return request.render('trademeda.wishlist_page',vals)
    
    @http.route(['/removeFromWishlist/<int:productId>'], type="http", auth="public", website=True)
    def RemoveFromWishlist(self, productId, **kwargs):
        user = request.env.user
        partner_id = user.partner_id

        wishlist_item = request.env['user.wishlist'].sudo().search([
            ('partner_id', '=', partner_id.id),
            ('product_id', '=', productId)
        ], limit=1)
        
        if wishlist_item:
            wishlist_item.sudo().unlink()

        return request.redirect('/wishlist')

    

    @http.route(['/is_logged_in',], type="http", auth="public", website=True)
    def loggedIn(self,**kw):
        user = request.env.user
        if user == request.env.ref('base.public_user'):
            vals = {
                'logged_in':False
            }
        else:
            vals = {
                'logged_in':True
            }
        return json.dumps(vals)
        
    @http.route(['/profile/updatenews'], methods=["POST"], type="http", auth="user", website=True)
    def UpdateNews(self, **kw):
        user = request.env.user
        partner_id = user.partner_id

        if request.httprequest.method == 'POST':
            news_title = kw.get('news-heading-text')
            news_image1 = kw.get('update_news1')
            news_image2 = kw.get('update_news2')
            news_image3 = kw.get('update_news3')
            news_image4 = kw.get('update_news4')
            news_image5 = kw.get('update_news5')
            news_content = kw.get('news-content')

            # Prepare the dictionary for updating partner fields
            update_vals = {
                'news_title': news_title,
                'news_text': news_content,
            }

            # Check if a new image is uploaded
            if news_image1:
                update_vals['news_image1'] = base64.b64encode(news_image1.read())
            if news_image2:
                update_vals['news_image2'] = base64.b64encode(news_image2.read())
            if news_image3:
                update_vals['news_image3'] = base64.b64encode(news_image3.read())
            if news_image4:
                update_vals['news_image4'] = base64.b64encode(news_image4.read())
            if news_image5:
                update_vals['news_image5'] = base64.b64encode(news_image5.read())

            partner_id.sudo().write(update_vals)

            return request.redirect("/profile")
        else:
            return request.redirect("/profile")
            

    @http.route(['/profile/getsubcategories/<int:category_id>'], methods=["GET"], type="http", auth="user", website=True)
    def getsubcategories(self,category_id, **kw):
        # import wdb;wdb.set_trace()

        # Logic to fetch subcategories based on category_id
        subcategories = request.env['product.subcategories'].sudo().search([('category_id.id', '=', category_id)])
        subcategory_list = [{
            'id': sub.id,
            'name': sub.name,
            # Add more fields as needed
        } for sub in subcategories]

        # Return JSON response

        return json.dumps(subcategory_list)
    
    @http.route(['/profile/getproducts/<int:subcategory_id>'], methods=["GET"], type="http", auth="user", website=True)
    def getproducts(self,subcategory_id, **kw):
        # import wdb;wdb.set_trace()
        products = request.env['product.template'].sudo().search([('subcategory_id.id','=',subcategory_id)])
        product_list = [{
            'id': sub.id,
            'name': sub.name,
            # Add more fields as needed
        } for sub in products]

        return json.dumps(product_list)

    
    
    

    # @http.route(['/supplier/sendenquiry'], methods=["POST"], type="http", auth="user", website=True)
    # def SendEnquiry(self, **kw):
    #     user = request.env.user
    #     partner_id = user.partner_id
        
    #     if request.httprequest.method == 'POST':
    #         message = kw.get('enquiry-message')
    #         name = kw.get('enquiry_user_name')
    #         email = kw.get('enquiry_user_email')
    #         phone = kw.get('enquiry_user_phone')
    #         country = kw.get('country')

    @http.route(['/supplier/sendproductenquiry/<int:user_id>'], methods=["POST"], type="json", auth="user", website=True, csrf=False)
    def SendProductEnquiry(self,user_id, **kw):
        # import wdb;wdb.set_trace()

        # user = request.env.user
        # partner_id = user.partner_id
        partner_id = request.env['res.partner'].sudo().search([('id','=',user_id)])
        # if data['product']:
        #     product_id = request.env['product.template'].sudo().search([('id','=',2)])


        try:
            data = request.httprequest.get_json()
        except Exception as e:
            return json.dumps({'error': 'Invalid JSON data', 'details': str(e)})

    
        partner_id.product_enquiries.sudo().create({
            'partner_id':user_id,
            'user_name':data['name'],
            'message':data['message'],
            'email':data['email'],
            'phone':data['phone'],
            'product_id':data['product'],
            'country':int(data['country'])
            
        })

        
            
    @http.route('/supplier/download_product_enquiries', type='http', auth='user', website=True)
    def download_product_enquiry(self):
        excel_buffer = io.BytesIO()

        # Create a new Excel workbook and add a worksheet
        workbook = xlsxwriter.Workbook(excel_buffer)
        enquiry_worksheet = workbook.add_worksheet("Product Enquiries")

        # Add headers
        headers = ['Name','Product', 'Email', 'Phone', 'Country', 'Message']
        for col_num, header in enumerate(headers):
            enquiry_worksheet.write(0, col_num, header)

        # Fetch the product enquiries
        enquiries = request.env['product.enquiries'].sudo().search([])

        # Write data to worksheet
        for row_num, enquiry in enumerate(enquiries, 1):
            enquiry_worksheet.write(row_num, 0, enquiry.user_name)
            enquiry_worksheet.write(row_num, 1, enquiry.product_id.name)
            enquiry_worksheet.write(row_num, 2, enquiry.email)
            enquiry_worksheet.write(row_num, 3, enquiry.phone)
            enquiry_worksheet.write(row_num, 4, enquiry.country.name)  # Assuming country_id is a Many2one field
            enquiry_worksheet.write(row_num, 5, enquiry.message)

        workbook.close()
        excel_buffer.seek(0)

        # Prepare the response with the appropriate headers
        response = request.make_response(excel_buffer.read(),
                                         headers=[
                                             ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                                             ('Content-Disposition', 'attachment; filename=product_enquiries.xlsx;')
                                         ])
        return response


    @http.route('/get_product_enquiries/<int:productId>', type='http', auth='user', website=True)
    def get_product_enquiry(self,productId,**kw):
        
        user = request.env.user
        partner_id = user.partner_id