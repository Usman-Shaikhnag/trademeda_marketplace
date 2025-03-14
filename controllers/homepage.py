from odoo import http
from odoo.http import request
import base64
import json
from odoo.exceptions import ValidationError
from datetime import timedelta, date
import os
import logging
_logger = logging.getLogger(__name__)

class HomepageController(http.Controller):

    @http.route('/home', auth='public', website=True)
    def home(self, **kwargs):
        user = request.env.user
        product_categories = request.env['product.categories'].sudo().search([])
        # import wdb;wdb.set_trace()

        # if user == request.env.ref('base.public_user'):
        #     logged_in:False
        # else:
        #     logged_in:True
        # import wdb;wdb.set_trace()
        
        vals = {
            "product_categories": product_categories,
            'logged_in':request.env.user != request.env.ref('base.public_user')
            }
        return request.render('trademeda.homepage',vals)
    
    @http.route('/', auth='public', website=True)
    def root(self, **kwargs):
        user = request.env.user
        product_categories = request.env['product.categories'].sudo().search([])

        
        vals = {
            "product_categories": product_categories,
            'logged_in':request.env.user != request.env.ref('base.public_user')
            }
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
    

    @http.route('/resetPassword', auth='public', website=True)
    def resetPassword(self, **kwargs):
        # import wdb;wdb.set_trace()
        
        return request.render('trademeda.resetPassword')
    
    @http.route('/forgotPassword', auth='public', website=True)
    def forgotPassword(self, **kwargs):
        # import wdb;wdb.set_trace()
        
        return request.render('trademeda.forgotPassword')

    @http.route('/contactus', auth='public', website=True)
    def contactus(self, **kwargs):
        # import wdb;wdb.set_trace()
        vals = {
            'contact':request.env['trademeda.conf'].sudo().search([],limit=1)
            }
        
        return request.render('trademeda.contactus',vals)
    
    @http.route('/logout', auth='user', website=True)
    def logout(self, **kwargs):
        # import wdb;wdb.set_trace()

        request.session.logout(keep_db=False)
        return request.redirect('/web/login')
    
    @http.route('/advertisingPlans', auth='public', website=True)
    def advertisingPlans(self, **kwargs):
        vals = {
            'logged_in':request.env.user != request.env.ref('base.public_user')
            }
        return request.render('trademeda.bannerApplication',vals)
    
    @http.route('/membershipPlans', auth='public', website=True)
    def membershipPlans(self, **kwargs):
        vals = {
            'logged_in':request.env.user != request.env.ref('base.public_user')
            }
        return request.render('trademeda.membershipPlans',vals)
    
    @http.route('/privacyPolicy', auth='public', website=True)
    def privacyPolicy(self, **kwargs):
        vals = {
            'logged_in':request.env.user != request.env.ref('base.public_user')
            }
        return request.render('trademeda.privacyPolicy',vals)
    
    @http.route('/product/<int:productId>', auth='public', website=True)
    def product(self,productId, **kwargs):
        user = request.env.user
        partner_id = user.partner_id
        product = request.env['product.customer.images'].sudo().search([('id','=',productId)])

        subcategory = request.env['product.subcategories'].sudo().search([('name','ilike',product.product_id.subcategory_id.name)])
        for sb in subcategory:
            # points = sb.points + 20
            sb.sudo().write({
                'points':sb.points + 1
            })
        vals = {
            'product':product,
            'logged_in':request.env.user != request.env.ref('base.public_user'),
            'partner':partner_id
        }
        return request.render('trademeda.product_details',vals)
    
    @http.route('/profile', auth='user', website=True)
    def UserProfile(self, **kwargs):

        user = request.env.user
        partner_id = user.partner_id
        # print("Partnerrrrr",partner_id)
        categories = request.env['product.categories'].sudo().search([])
        subcategories = request.env['product.subcategories'].sudo().search([])
        products = request.env['product.template'].sudo().search([])
        user_products = request.env['product.customer.images'].sudo().search([('partner_id','=',partner_id.id)])
        rfqs = request.env['trademeda.rfq'].sudo().search([('partner_id','=',partner_id.id),('state','!=','deleted')])


        vals = {
            'user':user,
            'partner':partner_id,
            'categories':categories,
            'subcategories':subcategories,
            'products':products,
            'user_products':user_products,
            'rfqs':rfqs,
            'logged_in':request.env.user != request.env.ref('base.public_user')

        }
        return request.render('trademeda.user_profile',vals)
    
    @http.route(['/my/products/subcategories'], type='http', auth="user")
    def get_subcategories(self, category_id):
        subcategories = request.env['product.subcategories'].sudo().search([('category_id', '=', int(category_id))])
        subcategory_list = [{'id': subcategory.id, 'name': subcategory.name} for subcategory in subcategories]
        # import wdb;wdb.set_trace()

        return {'subcategories': subcategory_list}
        
    @http.route(['/signup/createuser'], methods=["POST"], type="http", auth="public", website=True)
    def CreateUser(self, **kw):
        if request.httprequest.method == 'POST':
            # Extract form data
            name = kw.get("name")
            city = kw.get("city")
            member_type = kw.get('role')
            supplier_products = kw.get('supplier_textarea')
            buyer_products = kw.get('buyer_textarea')
            trader_products = kw.get('trader_textarea')
            primary_business = kw.get('business-type')
            establishment_year = kw.get('establishment_year')
            annual_sales = kw.get('annual-sales')
            employees =  kw.get('employees')
            designation = kw.get('designation')
            zip_code = kw.get("zip_code")
            country = kw.get("country")
            state = kw.get("state")
            phone = kw.get("phone_number")
            email = kw.get("email")
            password = kw.get("password")
            confirm_password = kw.get("confirm_password")
            address = kw.get('address')
            area_code = kw.get('area_code')
            company_email = kw.get('company_email')
            website = kw.get('website')
            company_name = kw.get('company_name')

            # import wdb;wdb.set_trace()
            # Basic validation
            if not all([name, city, zip_code, state, phone, email, password, confirm_password]):
                raise ValidationError("Not all required fields are filled")

            if password != confirm_password:
                raise ValidationError("Passwords do not match")
            

            portal_group = request.env.ref('base.group_portal')

            trademeda_conf = request.env['trademeda.conf'].sudo().search([],limit=1)

            if not trademeda_conf:
                raise ValidationError("Configuration not found")
            free_subscription_days = trademeda_conf.free_subscription_days

            
            try:
                # Create the partner first
                partner_data = {
                    'name': company_name,
                    'membership_state': 'free',
                    'free_member': True,
                    'company_type': 'company',
                    'member_type': member_type,
                    'supplier_products': supplier_products,
                    'buyer_products': buyer_products,
                    'trader_products': trader_products,
                    'primary_business': primary_business,
                    'establishment_year': int(establishment_year),
                    'annual_sales': annual_sales,
                    'no_of_employees':employees,
                    'user_name': name,
                    'designation': designation,
                    'country_id':int(country),
                    'state_id':int(state),
                    'street': address,
                    'country_id':int(country),
                    'city': city,
                    'zip': zip_code,
                    'phone': phone,
                    'area_code': area_code,
                    'email': email,
                    'website': website,
                    'subscription_remaining':int(free_subscription_days)
                }

                partner = request.env['res.partner'].sudo().create(partner_data)
                
                # Prepare user data for creation
                user_data = {
                    "login": email,
                    'password': password,
                    'name': name,
                    'partner_id': partner.id,  # Link the created partner
                    'groups_id': [(6, 0, [portal_group.id])]
                }

                # Create the user
                request.env['res.users'].sudo().create(user_data)

                mail = request.env['mail.mail'].sudo().create({
                    'subject': 'Your Trademeda Account has been created',
                    'body_html': f'<p>Your Trademeda Account has been created and you have been given free subscription of <strong>{free_subscription_days}</strong> days</p>',
                    'email_to': email,
                    'email_from': 'info@trademeda.com',
                })
                mail.send()

                return request.redirect("/signin")

            except Exception as e:
                # Handle exceptions, such as email already existing
                raise ValidationError("Something went wrong: %s" % str(e))

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
    

    

    @http.route(['/profile/updateuserprofile'], method=["POST"], type="http", auth="public", website=True)
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
            designation = kw.get('designation')
            address = kw.get('address')
            website = kw.get('company_website')
            logo = kw.get("upload_company_logo")
            company_image = kw.get("upload_company_image")
            role = kw.get('role')
            company_name = kw.get('company_name')



            
            data = {
                'name':name,
                'company_address':address,
                'phone':phone,
                'city':city,
                'zip':zip_code,
                'country_id':int(kw.get("country")),
                'state_id':int(state),
                'email':email,
                'member_type':role,
                'user_name':company_name,
                'company_website':website,
                'designation':designation                

            }
            # import wdb;wdb.set_trace()
            if logo:
                logo_filename = logo.filename
                logo_binary  = base64.b64encode(logo.read())
                data['logo_image'] = logo_binary
                data['logo_image_name'] = logo_filename
                
            if company_image:
                company_image_filename = company_image.filename
                company_image_binary  = base64.b64encode(company_image.read())
                data['company_image'] = company_image_binary
                data['company_image_name'] = company_image_filename


            # import wdb;wdb.set_trace()


            partner_id.sudo().write(data)
            return request.redirect("/profile")



    @http.route('/profile/supplier/<int:supplier_id>', auth='public', website=True)
    def supplier_profile(self,supplier_id,page=1, **kwargs):
        # import wdb;wdb.set_trace()
        user = request.env.user
        # partner_id = user.partner_id
        # items_per_page = 10
        # offset = (page - 1) * items_per_page
        products = request.env['product.customer.images'].sudo().search([('partner_id','=',supplier_id)])
        partner_id = request.env['res.partner'].sudo().search([('id','=',supplier_id)])

        # total_enquiries = partner_id.product_enquiries.sudo().search_count([])
        product_enquiries = partner_id.product_enquiries.sudo().search([], order='create_date desc')

        # pager = request.website.pager(
        #     url='/profile/supplier',
        #     total=total_enquiries,
        #     page=page,
        #     step=items_per_page
        # )

        vals = {
            "products": products,
            'partner':partner_id,
            'product_enquiries':product_enquiries,
            'logged_in':request.env.user != request.env.ref('base.public_user')
            # 'pager':pager

            }


        return request.render('trademeda.supplier_profile',vals)
    
    @http.route(['/deleteAward/<int:award_id>'], methods=["POST"], type="json", auth="user", website=True)
    def deleteAward(self, **kw):
        # import wdb;wdb.set_trace()
        user = request.env.user
        partner_id = user.partner_id
        award = request.env['customer.awards'].sudo().search([('partner_id.id','=',partner_id.id),('id','=',kw.get('award_id'))])
        award.sudo().unlink()
        # print("Partnerrrrr",partner_id)
        
    @http.route(['/deleteUser/<int:user_id>'], methods=["POST"], type="json", auth="user", website=True)
    def deleteUser(self, **kw):
        # import wdb;wdb.set_trace()
        user = request.env.user
        partner_id = user.partner_id
        user = request.env['customer.employees'].sudo().search([('partner_id.id','=',partner_id.id),('id','=',kw.get('user_id'))])
        user.sudo().unlink()
    
    

    @http.route(['/profile/updatedocuments'], method=["POST"], type="http", auth="user", website=True)
    def UpdateDocuments(self, **kw):
        # import wdb;wdb.set_trace()
        
        user = request.env.user
        partner_id = user.partner_id
        if request.httprequest.method == 'POST':
            # update_award_id = None
            # for key, value in kw.items():
            #     if key.startswith('update_award_'):
            #         update_award_id = int(key.split('_')[-1])
            award_list = []
            award_name_list = []
            award_description_list = []

            for rec in kw:
                if "new_award" in rec:
                    award_list.append(kw.get(rec))
            for rec in kw:
                if "new_name_" in rec:
                    award_name_list.append(kw.get(rec))
            for rec in kw:
                if "new_description_" in rec:
                    award_description_list.append(kw.get(rec))

            combined_list = []

            
            for award_file, award_name, award_description in zip(award_list, award_name_list, award_description_list):
                # import wdb;wdb.set_trace()
                combined_list.append({
                    'award_file': award_file.read(),
                    'award_name': award_name,
                    'award_description': award_description,
                    'file_name':award_file.filename
            })

            for award in combined_list:
                award_file = award.get('award_file')
                award_name = award.get('award_name')
                file_name = award.get('file_name')

                award_description = award.get('award_description')

                
                # Read the file content and encode it to base64
                if award_file:
                    award_file_content = award_file
                    award_file_encoded = base64.b64encode(award_file_content)
                else:
                    award_file_encoded = None  # Handle cases where no file is provided

                # Create the award record
                partner_id.awards.sudo().create({
                    'partner_id': partner_id.id,
                    'award_name': award_name,
                    'file_name':file_name,
                    'award_attachment': award_file_encoded,
                    'award_description':award_description
                })
            # certificates 
            certificate_list = []
            certificate_name_list = []
            certificate_description_list = []

            for rec in kw:
                if "new_certificate" in rec:
                    certificate_list.append(kw.get(rec))
            for rec in kw:
                if "new_cert_name_" in rec:
                    certificate_name_list.append(kw.get(rec))
            for rec in kw:
                if "new_cert_description_" in rec:
                    certificate_description_list.append(kw.get(rec))
            

            combined_list = []
            # import wdb;wdb.set_trace()

            
            for certificate_file, certificate_name, certificate_description in zip(certificate_list, certificate_name_list, certificate_description_list):
                # import wdb;wdb.set_trace()
                combined_list.append({
                    'certificate_file': certificate_file.read(),
                    'certificate_name': certificate_name,
                    'certificate_description': certificate_description,
                    'file_name':certificate_file.filename
            })

            for certificate in combined_list:
                certificate_file = certificate.get('certificate_file')
                certificate_name = certificate.get('certificate_name')
                file_name = certificate.get('file_name')

                certificate_description = certificate.get('certificate_description')

                
                # Read the file content and encode it to base64
                if certificate_file:
                    certificate_file_content = certificate_file
                    certificate_file_encoded = base64.b64encode(certificate_file_content)
                else:
                    certificate_file_encoded = None  # Handle cases where no file is provided

                # Create the certificate record
                partner_id.certificates.sudo().create({
                    'partner_id': partner_id.id,
                    'certificate_name': certificate_name,
                    'file_name':file_name,
                    'certificate_attachment': certificate_file_encoded,
                    'certificate_description':certificate_description
                })

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
        user = request.env.user
        partner_id = user.partner_id

        # Extract form data
        product_name = kw.get('product_name')
        product_description = kw.get('product_description')
        product_subsubcategory = kw.get('product_subsubcategory')
        product_quantity = kw.get('quantity')
        product_unit = kw.get('quantity_unit')


        # Read the product images and names if they exist
        product_image = kw.get('upload_product')
        product_image1 = kw.get('upload_product1')
        product_image2 = kw.get('upload_product2')
        product_image3 = kw.get('upload_product3')

        image_name = kw.get('image_name')
        image_name1 = kw.get('image_name1')
        image_name2 = kw.get('image_name2')
        image_name3 = kw.get('image_name3')
        buyer_country = kw.get('buyers_country')

        # Prepare data for the record creation
        product_data = {
            'partner_id': partner_id.id,
            'product_name': product_name,
            'product_description': product_description,
            'product_id': product_subsubcategory,
            'product_quantity': product_quantity,
            'unit': product_unit,
            'payment_mode':kw.get('payment_terms'),
            'shipping_terms':kw.get('shipping_terms'),
            
        }
        if buyer_country:
            product_data['buyers_country'] = int(buyer_country)
        # Add product images if they are uploaded
        if product_image:
            product_data['product_image'] = base64.b64encode(product_image.read())
            product_data['image_name'] = image_name

        if product_image1:
            product_data['product_image2'] = base64.b64encode(product_image1.read())
            product_data['image_name2'] = image_name1

        if product_image2:
            product_data['product_image3'] = base64.b64encode(product_image2.read())
            product_data['image_name3'] = image_name2

        if product_image3:
            product_data['product_image4'] = base64.b64encode(product_image3.read())
            product_data['image_name4'] = image_name3

        # Create the product record with the images and descriptions
        product = partner_id.product_images.sudo().create(product_data)
        product_subcategory = request.env['product.template'].sudo().search([('id','=',product_subsubcategory)]).subcategory_id
        # subscribers = request.env['res.partner'].sudo().search([('subscribed_categories', 'in', product_subcategory.id),('member_type','in',['buyer','both'])])
        subscribers = request.env['res.partner'].sudo().search([
            ('subscribed_categories', 'in', [product_subcategory.id]),  # Ensure it's in a list
            ('member_type', 'in', ['buyer', 'both']),  # Filter by member_type
            ('id','!=',partner_id.id)
        ])
            # import wdb;wdb.set_trace()
            
        for subscriber in subscribers:
            request.env['subscribed.notifications'].sudo().create({
                'partner_id': subscriber.id, 
                'notification': f'1 New Supplier posted sale offer for {product_name}',
                'seller_notification':False,
                'buyer_notification':True,
                'product_id':product.id
            })

        return request.redirect("/profile")
        
    @http.route('/get_categories/<string:dataId>', type='http', auth='user',website=True)
    def get_categoriess(self,dataId, **kw):
        categories = request.env['product.categories'].sudo().search([('category_type', '=', dataId)])
        # import wdb;wdb.set_trace()
        # categories_data = [{'id': category.id, 'name': category.name} for category in categories]
        # return Response(json.dumps(categories_data), content_type='application/json', status=200)

        categories = request.env['product.categories'].sudo().search([('category_type', '=', dataId)])
        category_list = [{
            'id': cat.id,
            'name': cat.name,
            # Add more fields as needed
        } for cat in categories]

        # Return JSON response

        return json.dumps(category_list)
    
    

    
    
    
    @http.route('/deleterfq', methods=['POST'], type='json', auth='user', website=True)
    def deleteRfq(self, **kwargs):
        user = request.env.user
        partner_id = user.partner_id
        data = request.httprequest.get_json()
        
        if data:
            rfq = request.env['trademeda.rfq'].sudo().search([('id', '=', int(data['rfqId'])), ('partner_id', '=', partner_id.id)])
            if rfq:
                try:
                    rfq.sudo().write({'state': 'deleted'})
                    return request.redirect('/profile')
                except Exception as e:
                    return request.redirect('/profile')

        return {'status': 'error', 'message': 'RFQ not found or deletion failed'}
    
    @http.route('/endRfq', methods=['POST'], type='json', auth='user', website=True)
    def endRfq(self, **kwargs):
        user = request.env.user
        partner_id = user.partner_id
        data = request.httprequest.get_json()
        
        if data:
            rfq = request.env['trademeda.rfq'].sudo().search([('id', '=', int(data['rfqId'])), ('partner_id', '=', partner_id.id)])
            if rfq:
                try:
                    rfq.sudo().write({'state': 'closed'})
                    return request.redirect('/profile')
                except Exception as e:
                    return request.redirect('/profile')

        return {'status': 'error', 'message': 'RFQ not found or operation failed'}

    @http.route('/categories', auth='public', website=True)
    def categoriesPage(self, **kwargs):
        vals = {
            'logged_in':request.env.user != request.env.ref('base.public_user')
        }
        return request.render('trademeda.categories',vals)
    

    @http.route('/categories/<int:category_id>', auth='public', website=True)
    def subcategoriesPage(self,category_id, **kwargs):
        products = request.env['product.template'].sudo().search([('subcategory_id.id','=',category_id)])
        category = request.env['product.subcategories'].sudo().search([('id','=',category_id)],limit=1)
        vals = {
            'products':products,
            'category':category
        }
        return request.render('trademeda.subcategories',vals)
    
    @http.route('/countries', auth='public', website=True)
    def countries(self, **kwargs):
        user = request.env.user
        countries = request.env['res.country'].sudo().search([])
        # if user == request.env.ref('base.public_user'):
        #     logged_in:False
        # else:
        #     logged_in:True
        # import wdb;wdb.set_trace()
        
        vals = {
            "countries": countries,
            'logged_in':request.env.user != request.env.ref('base.public_user')
            }
        return request.render('trademeda.countries',vals)
    

    @http.route('/brochure', auth='public', website=True)
    def brochure(self, **kwargs):
        user = request.env.user
       
        vals = {
            'logged_in':request.env.user != request.env.ref('base.public_user')
            }
        return request.render('trademeda.brochure',vals)
    
    @http.route('/terms_conditions', auth='public', website=True)
    def terms_conditions(self, **kwargs):
        user = request.env.user
       
        vals = {
            'logged_in':request.env.user != request.env.ref('base.public_user')
            }
        return request.render('trademeda.terms_conditions',vals)
    
    @http.route('/productListingPolicy', auth='public', website=True)
    def productListingPolicy(self, **kwargs):
        user = request.env.user
       
        vals = {
            'logged_in':request.env.user != request.env.ref('base.public_user')
            }
        return request.render('trademeda.product_listing',vals)
    
    @http.route('/apply_testimony', auth='user', website=True)
    def applyTestimony(self, **kwargs):
        return request.render('trademeda.testimony_application')
    
    @http.route('/feedback', auth='user', website=True)
    def applyFeedback(self, **kwargs):
        return request.render('trademeda.feedback_application')


    @http.route('/submit_testimony', type='http', auth='user', methods=['POST'], csrf=False)
    def submit_testimony(self, **kw):
        user = request.env.user
        partner_id = user.partner_id
        testimony = kw.get('testimony')
        request.env['customer.testimony'].sudo().create({
            'testimony':testimony,
            'partner_id':partner_id.id
        })
        return request.render('trademeda.homepage')
    
    @http.route('/submit_feedback', type='http', auth='user', methods=['POST'], csrf=False)
    def submit_feedback(self, **kw):
        user = request.env.user
        partner_id = user.partner_id
        feedback = kw.get('feedback')
        request.env['customer.feedback'].sudo().create({
            'feedback':feedback,
            'partner_id':partner_id.id
        })
        return request.render('trademeda.homepage')

    @http.route('/aboutus', auth='public', website=True)
    def aboutus(self, **kwargs):
        user = request.env.user
        
        vals = {
            'logged_in':request.env.user != request.env.ref('base.public_user')
            }
        return request.render('trademeda.aboutus',vals)
    
    @http.route('/trustscore', auth='public', website=True)
    def trustscore(self, **kwargs):
        user = request.env.user
        
        vals = {
            'logged_in':request.env.user != request.env.ref('base.public_user')
            }
        return request.render('trademeda.trustscore',vals)

    @http.route('/faqs', auth='public', website=True)
    def faqpage(self, **kwargs):
        user = request.env.user
        
        vals = {
            'logged_in':request.env.user != request.env.ref('base.public_user')
            }
        return request.render('trademeda.faq_portal',vals)
    
    @http.route('/mission', auth='public', website=True)
    def mission(self, **kwargs):
        user = request.env.user
        
        vals = {
            'logged_in':request.env.user != request.env.ref('base.public_user')
            }
        return request.render('trademeda.mission',vals)

    



    @http.route(['/get_states'], methods=["POST"],  type="json", auth="public")
    def get_states(self):
        # import wdb;wdb.set_trace()
        country_id = request.httprequest.json.get('country_id')

        if not country_id:
            return {'error': 'Country ID not provided'}

        states = request.env['res.country.state'].sudo().search([('country_id', '=', int(country_id))])
        state_list = [{'id': state.id, 'name': state.name} for state in states]

        return {'state_list': state_list}
    
    @http.route('/checkPassword', methods=["POST"], type="json", auth='public')
    def checkPassword(self):
        email = request.httprequest.json.get('email')
        old_password = request.httprequest.json.get('old_password')
        
        # Check if email is provided
        # import wdb;wdb.set_trace()


        if not email:
            return {'status': 'error', 'message': 'Email not provided'}, 400  # HTTP 400 for missing data
        if not old_password:
            return {'status': 'error', 'message': 'Password not provided'}, 400  # HTTP 400 for missing data
        
        

        # Search for an existing user with the specified email
        existing_user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)

        if not existing_user._check_password(old_password):
             return {'status': 'error', 'message': 'Incorrect Password'}, 300
        
        # Check if the user exists and respond accordingly
        if not existing_user:
            return {'status': 'error', 'message': 'Email doesnt exists'}, 409  # HTTP 409 Conflict for duplicate
        return {'status': 'success', 'message': ''}, 200
    

    @http.route('/changePassword', methods=["POST"], type="http", auth='public')
    def change_password(self,**kw):
        # import wdb;wdb.set_trace()

        email = kw.get('email')
        old_password = kw.get('old_password')
        new_password = kw.get('new_password')

        # if old_password == new_password:
        #     return {'error': 'New password cannot be same'}

        

        user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)

        if not user:
            return {'error': 'User not found'}

        # Verify old password
        try:
            request.session.authenticate(request.db, email, old_password)
        except:
            return {'error': 'Incorrect old password'}

        # Update password
        user.sudo().write({'password': new_password})

        return request.redirect("/signin")
        

    @http.route('/forgotPassword/reset', methods=["POST"], type="http", auth='public')
    def forgot_password(self,**kw):
        # import wdb;wdb.set_trace()

        email = kw.get('email')
        # old_password = kw.get('old_password')
        new_password = kw.get('new_password')

        user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)

        if not user:
            return {'error': 'User not found'}

        
        # Update password
        user.sudo().write({'password': new_password})

        return request.redirect("/signin")
        