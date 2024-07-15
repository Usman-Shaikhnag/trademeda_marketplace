from odoo import http
from odoo.http import request
import base64
import json
class ProductController(http.Controller):

    @http.route(['/add-to-favourites/<int:product_id>',], type="http", auth="public", website=True)
    def AddToFavourite(self, **kwargs):

        user = request.env.user
        partner_id = user.partner_id

        if user == request.env.ref('base.public_user'):
        

        
            return request.render('trademeda.user_profile')
        
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
        subcategories = request.env['product.subcategories'].sudo().search([('category.id', '=', category_id)])
        subcategory_list = [{
            'id': sub.id,
            'name': sub.name,
            # Add more fields as needed
        } for sub in subcategories]

        # Return JSON response

        return json.dumps(subcategory_list)
    
    