from odoo import http
from odoo.http import request
import base64
import json
import io
import xlsxwriter
from io import BytesIO
import xlrd
import logging

_logger = logging.getLogger(__name__)
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
        # import wdb;wdb.set_trace()
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
            'products': actual_products,
            'logged_in':request.env.user != request.env.ref('base.public_user')
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
    
    @http.route('/buyer/download_rfq_enquiries/<int:rfq_id>', type='http', auth='user', website=True)
    def download_buyers_rfq_enquiries(self,rfq_id):
        user = request.env.user
        partner_id = user.partner_id

        excel_buffer = io.BytesIO()
        # import wdb;wdb.set_trace()

        # Create a new Excel workbook and add a worksheet
        workbook = xlsxwriter.Workbook(excel_buffer)
        quotation_worksheet = workbook.add_worksheet("RFQs")

        headers = ['Date','RFQ No','Company Name', 'Email', 'Phone','Country', 'Message','Supplier']
        for col_num, header in enumerate(headers):
            quotation_worksheet.write(0, col_num, header)

        # Fetch the product enquiries
        quotations = request.env['rfq.quotations'].sudo().search([('rfq_id','=',rfq_id)],order='create_date desc')

        # Write data to worksheet
        for row_num, quotation in enumerate(quotations, 1):
            quotation_worksheet.write(row_num, 0, quotation.create_date.strftime('%d-%b-%Y'))
            quotation_worksheet.write(row_num, 1, quotation.rfq_id.rfq_no)
            quotation_worksheet.write(row_num, 2 , quotation.company_name)
            quotation_worksheet.write(row_num, 3, quotation.email)
            quotation_worksheet.write(row_num, 4, quotation.phone)
            quotation_worksheet.write(row_num, 5, quotation.country_id.name)  # Assuming country_id is a Many2one field
            quotation_worksheet.write(row_num, 6 , quotation.message)
            quotation_worksheet.write(row_num, 7 , quotation.partner_id.name)



        workbook.close()
        excel_buffer.seek(0)

        # Prepare the response with the appropriate headers
        response = request.make_response(excel_buffer.read(),
                                         headers=[
                                             ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                                             ('Content-Disposition', 'attachment; filename=rfq_quotations.xlsx;')
                                         ])
        return response


    @http.route('/supplier/download_rfqs', type='http', auth='user', website=True)
    def download_rfqs(self):

        user = request.env.user
        partner_id = user.partner_id

        excel_buffer = io.BytesIO()
        # import wdb;wdb.set_trace()

        # Create a new Excel workbook and add a worksheet
        workbook = xlsxwriter.Workbook(excel_buffer)
        quotation_worksheet = workbook.add_worksheet("RFQs")

        # Add headers
        headers = ['Date','RFQ No','Company Name', 'Email', 'Phone','Country', 'Message','Buyer']
        for col_num, header in enumerate(headers):
            quotation_worksheet.write(0, col_num, header)

        # Fetch the product enquiries
        quotations = request.env['rfq.quotations'].sudo().search([('partner_id','=',partner_id.id)],order='create_date desc')

        # Write data to worksheet
        for row_num, quotation in enumerate(quotations, 1):
            quotation_worksheet.write(row_num, 0, quotation.create_date.strftime('%d-%b-%Y'))
            quotation_worksheet.write(row_num, 1, quotation.rfq_id.rfq_no)
            quotation_worksheet.write(row_num, 2 , quotation.company_name)
            quotation_worksheet.write(row_num, 3, quotation.email)
            quotation_worksheet.write(row_num, 4, quotation.phone)
            quotation_worksheet.write(row_num, 5, quotation.country_id.name)  # Assuming country_id is a Many2one field
            quotation_worksheet.write(row_num, 6 , quotation.message)
            quotation_worksheet.write(row_num, 7 , quotation.rfq_id.partner_id.name)



        workbook.close()
        excel_buffer.seek(0)

        # Prepare the response with the appropriate headers
        response = request.make_response(excel_buffer.read(),
                                         headers=[
                                             ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                                             ('Content-Disposition', 'attachment; filename=product_quotations.xlsx;')
                                         ])
        return response


    @http.route('/get_product_enquiries/<int:productId>', type='http', auth='user', website=True)
    def get_product_enquiry(self,productId,**kw):
        
        user = request.env.user
        partner_id = user.partner_id


    @http.route(['/profile/getProduct/<int:product_id>'], type="http", auth="user", website=True)
    def getProduct(self, product_id, **kwargs):
        user = request.env.user
        partner_id = user.partner_id
        product = request.env['product.customer.images'].sudo().search([('id','=',product_id)])
        if product:
            product_image_base64 = base64.b64encode(product.product_image or b'').decode('utf-8')
            vals = {
                'product_name':product.product_id.name,
                'variety':product.product_variety_name,
                'quantity':product.product_quantity,
                'product_description':product.product_description,
                'product_image':product_image_base64

            }
            return json.dumps(vals)


    @http.route(['/profile/updateproduct/<int:product_id>'], methods=["POST"], type="http", auth="user", website=True)
    def updateProduct(self, product_id, **kw):
        user = request.env.user
        partner_id = user.partner_id
        # import wdb;wdb.set_trace()
        product = request.env['product.customer.images'].sudo().search([('id','=',product_id),('partner_id','=',partner_id.id)],limit=1)

        for rec in kw:
            if "update_product_image_" in rec:
                    update_product_image = kw.get(rec).read()
        for rec in kw:
            if "edit_delivery_days_" in rec:
                    edit_delivery_days = kw.get(rec)
            
        for rec in kw:
            if "edit_packaging_requirement" in rec:
                    edit_packaging_requirement = kw.get(rec)
            
        for rec in kw:
            if "edit_payment_mode_" in rec:
                    edit_payment_mode = kw.get(rec)
            
        for rec in kw:
            if "edit_product_description_" in rec:
                    edit_product_description = kw.get(rec)
            
        for rec in kw:
            if "edit_product_price_usd_" in rec:
                    edit_product_price_usd = kw.get(rec)
            
        for rec in kw:
            if "edit_product_quantity_" in rec:
                    edit_product_quantity = kw.get(rec)
            
        for rec in kw:
            if "edit_rts_quantity_" in rec:
                    edit_rts_quantity = kw.get(rec)
        for rec in kw:
            if "edit_sample_policy_" in rec:
                    edit_sample_policy = kw.get(rec)
            
        for rec in kw:
            if "ready_to_buy_requirements" in rec:
                    if kw.get(rec) == 'yes':
                        ready_to_buy_requirements = True
                    else:
                        ready_to_buy_requirements = False

        if product:
            if update_product_image:
                product.sudo().write({
                    'product_image':base64.b64encode(update_product_image),
                    'image_name':update_product_image.filename,
                    'product_description':edit_product_description,
                    'product_quantity':edit_product_quantity,
                    'packaging_requirement':edit_packaging_requirement,
                    'delivery_days':edit_delivery_days,
                    'product_price_usd':edit_product_price_usd,
                    'payment_mode':edit_payment_mode,
                    'sample_policy':edit_sample_policy,
                    'rts_quantity':edit_rts_quantity,
                    'ready_to_ship':ready_to_buy_requirements
                })
            else:
                 product.sudo().write({
                    'product_description':edit_product_description,
                    'product_quantity':edit_product_quantity,
                    'packaging_requirement':edit_packaging_requirement,
                    'delivery_days':edit_delivery_days,
                    'product_price_usd':edit_product_price_usd,
                    'payment_mode':edit_payment_mode,
                    'sample_policy':edit_sample_policy,
                    'rts_quantity':edit_rts_quantity,
                    'ready_to_ship':ready_to_buy_requirements
                })
        return request.redirect("/profile")
            
            
                
    
    @http.route(['/profile/uploadtemp'], methods=["POST"], type="http", auth="user", website=True)
    def uploadTemp(self, **kw):
        _logger.info('Upload subcategories started.')

        file_content = kw.get("upload_temp").read()
        workbook = xlrd.open_workbook(file_contents=file_content)
        worksheet = workbook.sheet_by_index(2)  # Third sheet

        # Read the header row to get the subcategory names
        header_row = worksheet.row_values(0)
        _logger.info(f'Header row: {header_row}')
        
        # Dictionary to store subcategory objects for quick lookup
        subcategory_dict = {}

        # Iterate through the rows to get the sub-subcategories for each subcategory
        for row_num in range(1, worksheet.nrows):
            row = worksheet.row_values(row_num)
            _logger.info(f'Processing row {row_num}: {row}')
            for col_num, cell_value in enumerate(row):
                if cell_value.strip():  # Check if cell value is not empty
                    subcategory_name = header_row[col_num].strip()
                    subsubcategory_name = cell_value.strip()

                    _logger.info(f'Processing subcategory: {subcategory_name}, subsubcategory: {subsubcategory_name}')

                    if subcategory_name not in subcategory_dict:
                        # Search for the subcategory
                        subcategory = request.env['product.subcategories'].sudo().search([('name', '=', subcategory_name)], limit=1)
                        if subcategory:
                            subcategory_dict[subcategory_name] = subcategory
                            _logger.info(f'Subcategory found: {subcategory_name}')
                        else:
                            # If the subcategory does not exist, skip to the next cell
                            _logger.info(f'Subcategory not found: {subcategory_name}')
                            continue
                    else:
                        subcategory = subcategory_dict[subcategory_name]

                    # Create sub-subcategory under the subcategory
                    request.env['product.template'].sudo().create({
                        'name': subsubcategory_name,
                        'subcategory_id': subcategory.id,
                    })
                    _logger.info(f'Subsubcategory created: {subsubcategory_name}')

        _logger.info('Upload subcategories finished.')

        return 

        
    @http.route(['/submitRfq'], method=["POST"], type="http", auth="user", website=True)
    def submitRfq(self, **kw):
        user = request.env.user
        partner_id = user.partner_id

        # import wdb;wdb.set_trace()
        if request.httprequest.method == 'POST':

            request_type = kw.get('request_type')
            subcategories = request.env['product.subcategories'].sudo().search([('id','=',int(kw.get('product_subcategory')))])
            subsubcategories = request.env['product.template'].sudo().search([('id','=',int(kw.get('product_subsubcategory')))])  
            product = kw.get('product')
            quantity = kw.get('quantity')
            unit = request.env['uom.uom'].sudo().search([('id','=',kw.get('unit'))])
            product_specification = kw.get('product_specification')
            target_price = kw.get('target_price')
            shipping_terms = kw.get('shipping_terms')
            payment_terms = kw.get('payment_terms')
            if kw.get('supplier_country') != '':
                supplier_country = request.env['res.country'].sudo().search([('id','=',kw.get('supplier_country'))]).id
            else:
                supplier_country = False
            if kw.get('destination') != '':
                destination = request.env['res.country'].sudo().search([('id','=',kw.get('destination'))]).id
            else:
                destination = False
            if kw.get('currency') != '':
                currency = request.env['res.country'].sudo().search([('id','=',kw.get('currency'))]).id
            else:
                currency = False
            if kw.get('upload_product'):
                product_image = kw.get('upload_product').read()
            else:
                product_image = None
            contact_person = kw.get('contact_person')

            if product_image:

                request.env['trademeda.rfq'].sudo().create({
                    'request_type':request_type,
                    'partner_id':partner_id.id,
                    'subcategory':subcategories.id,
                    'product_subsubcategory':subsubcategories.id,
                    'product_name':product,
                    'quantity':quantity,
                    'unit':unit.id,
                    'product_description':product_specification,
                    'target_price':target_price,
                    'currency':currency,
                    'destination':destination,
                    'shipping_terms':shipping_terms,
                    'payment_terms':payment_terms,
                    'suppliers_country':supplier_country,
                    'contact_person_name':contact_person,
                    'product_image':base64.b64encode(product_image),

                })
            else:
                request.env['trademeda.rfq'].sudo().create({
                    'request_type':request_type,
                    'partner_id':partner_id.id,
                    'subcategory':subcategories.id,
                    'product_subsubcategory':subsubcategories.id,
                    'product_name':product,
                    'quantity':quantity,
                    'unit':unit.id,
                    'product_description':product_specification,
                    'target_price':target_price,
                    'currency':currency,
                    'destination':destination,
                    'shipping_terms':shipping_terms,
                    'payment_terms':payment_terms,
                    'suppliers_country':supplier_country,
                    'contact_person_name':contact_person,

                })
            points = subsubcategories.subcategory_id.points + 100
            subsubcategories.subcategory_id.sudo().write({
                'points':points
            })
            return request.redirect('/home')
        


    @http.route(['/profile/updateusers'], methods=["POST"], type="http", auth="user", website=True)
    def UpdateUsers(self, **kw):
        # import wdb;wdb.set_trace()
        user = request.env.user
        partner_id = user.partner_id
        if request.httprequest.method == 'POST':

            username_list = []
            userdesignation_list = []
            contact_list = []
            email_list = []


            for rec in kw:
                if "new_user_" in rec:
                    username_list.append(kw.get(rec))
            for rec in kw:
                if "new_user_designation_" in rec:
                    userdesignation_list.append(kw.get(rec))
            for rec in kw:
                if "new_user_contact" in rec:
                    contact_list.append(kw.get(rec))
            for rec in kw:
                if "new_user_email" in rec:
                    email_list.append(kw.get(rec))

            combined_list = []

        for user_name, user_designation, user_contact,user_email in zip(username_list, userdesignation_list, contact_list,email_list):
                # import wdb;wdb.set_trace()
                combined_list.append({
                    'user_name': user_name,
                    'user_designation': user_designation,
                    'user_contact':user_contact,
                    'user_email':user_email

            })
        for user in combined_list:
                username = user.get('user_name')
                userdesignation = user.get('user_designation')
                userContact = user.get('user_contact')
                userEmail = user.get('user_email')



                
               
                partner_id.customer_employees.sudo().create({
                    'partner_id': partner_id.id,
                    'employee_name': username,
                    'employee_designation': userdesignation,
                    'employee_contact': userContact,
                    'employee_email': userEmail

                    
                })
       
        return request.redirect('/profile')

    @http.route(['/profile/updateProduct/<int:productId>'], methods=["POST"], type="json", auth="user", website=True)
    def UpdateProduct(self, productId, **kw):
        # import wdb;wdb.set_trace()

        user = request.env.user
        partner_id = user.partner_id
        
        if request.httprequest.json:
            data = request.httprequest.json
            
            # Extracting fields from the JSON payload
            delivery_days = data['delivery_days']
            packaging_requirement = data['packaging_requirement']
            payment_mode = data['payment_mode']
            product_description = data['product_description']
            product_price_usd = data['product_price_usd']
            product_quantity = data['product_quantity']
            ready_to_ship = data['ready_to_ship']
            rts_quantity = data['rts_quantity']
            sample_policy = data['sample_policy']
            product_image = data.get('product_image')

            # Searching for the product associated with the current partner
            product = request.env['product.customer.images'].sudo().search([
                ('id', '=', productId),
                ('partner_id', '=', partner_id.id)
            ])

            # Prepare the values to be updated
            update_vals = {
                'product_description': product_description,
                'product_quantity': product_quantity,
                'delivery_days': delivery_days,
                'product_price_usd': product_price_usd,
                'sample_policy': sample_policy,
                'ready_to_ship': ready_to_ship,
                'rts_quantity': rts_quantity,
                'packaging_requirement': packaging_requirement,
                'payment_mode': payment_mode
            }

            # If there's a product image, decode it from base64 and add to update_vals
            if product_image:
                update_vals['product_image'] = base64.b64decode(product_image)

            # Updating the product record
            product.sudo().write(update_vals)
        else:
            return


