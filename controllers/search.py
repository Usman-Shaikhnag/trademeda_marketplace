from odoo import http
from odoo.http import request
import base64
import json
import math
import ast

class SearchController(http.Controller):


    @http.route('/findSuppliers/<string:product>', method=['GET'], type='http', auth='public', website=True)
    def searchSupplierProduct(self, product,country_ids=[], page=1, **kw):
        per_page = 20  # Number of suppliers per page
        offset = (int(page) - 1) * per_page

        
        supplier_domain = ['|', '|', 
                   ('product_id.name', 'ilike', product), 
                   ('product_name', 'ilike', product), 
                   ('partner_id.name', 'ilike', product)]
        buyer_domain = ['|', ('product_subsubcategory.name', 'ilike', product), ('product_name', 'ilike', product)]
        # import wdb;wdb.set_trace()
        if country_ids:
            country_ids = ast.literal_eval(country_ids)
            country_ids = list(set(country_ids))
            supplier_domain = ['&', ('partner_id.country_id.id', 'in', country_ids)] + supplier_domain
            buyer_domain = ['&', ('partner_id.country_id.id', 'in', country_ids)] + buyer_domain
        
        
        user = request.env.user
        partner_id = user.partner_id

        if product:
            suppliers = request.env['product.customer.images'].sudo().search(supplier_domain,limit=per_page, offset=offset
            )
            total_suppliers = request.env['product.customer.images'].sudo().search_count(supplier_domain)
            buyers = request.env['trademeda.rfq'].sudo().search(buyer_domain)
        else:
            suppliers = request.env['product.customer.images'].sudo().search([], limit=per_page, offset=offset)
            total_suppliers = request.env['product.customer.images'].sudo().search_count([])
            buyers = request.env['trademeda.rfq'].sudo().search([])

        related_products = request.env['product.template'].sudo().search([('name', 'ilike', product)], limit=10)
        unique_subcategories = set()
        related_subcategories = []

        for rel_product in related_products:
            category = rel_product.subcategory_id.category_id
            if category:
                subcategories_in_category = request.env['product.subcategories'].sudo().search(
                    [('category_id', '=', category.id)]
                )

                for subcategory in subcategories_in_category:
                    subcategory_name = subcategory.name
                    if subcategory_name and subcategory_name not in unique_subcategories:
                        unique_subcategories.add(subcategory_name)
                        related_subcategories.append({'name': subcategory_name})
                    if len(unique_subcategories) >= 5:
                        break
            if len(unique_subcategories) >= 5:
                break

        total_pages = (total_suppliers + per_page - 1) // per_page  # Calculate the total number of pages

        vals = {
            'suppliers': suppliers,
            'buyers': buyers,
            'query': product,
            'related_products': related_products,
            'related_subcategories': unique_subcategories,
            'supplier_search': True,
            'buyer_search': False,
            'page': page,
            'total_pages': total_pages,
            'partner':partner_id,
            'country_ids':country_ids,
            'logged_in':request.env.user != request.env.ref('base.public_user')
        }
        return request.render("trademeda.findSuppliers", vals)

    

    @http.route('/findBuyers/<string:product>', method=['GET'], type='http', auth='public', website=True)
    def searchBuyerProduct(self, product,country_ids=[], page=1, **kw):
        per_page = 20  # Number of buyers per page
        offset = (int(page) - 1) * per_page
        # import wdb;wdb.set_trace()
        
        
        # supplier_domain = ['|', ('product_id.name', 'ilike', product), ('product_name', 'ilike', product)]
        supplier_domain = ['|', '|', 
                   ('product_id.name', 'ilike', product), 
                   ('product_name', 'ilike', product), 
                   ('partner_id.name', 'ilike', product)]
        buyer_domain = ['|', ('product_subsubcategory.name', 'ilike', product), ('product_name', 'ilike', product)]

        user = request.env.user
        partner_id = user.partner_id

        if product:
            if country_ids:
                country_ids = ast.literal_eval(country_ids)
                country_ids = list(set(country_ids))
            else:
                country_ids = []
            suppliers = request.env['product.customer.images'].sudo().search(supplier_domain)
            buyers = request.env['trademeda.rfq'].sudo().search(buyer_domain,limit=per_page, offset=offset)
            total_buyers = request.env['trademeda.rfq'].sudo().search_count(buyer_domain)
        else:
            suppliers = request.env['product.customer.images'].sudo().search([])
            buyers = request.env['trademeda.rfq'].sudo().search([], limit=per_page, offset=offset)
            total_buyers = request.env['trademeda.rfq'].sudo().search_count([])

        related_products = request.env['product.template'].sudo().search([('name', 'ilike', product)], limit=10)
        unique_subcategories = set()
        related_subcategories = []

        for rel_product in related_products:
            category = rel_product.subcategory_id.category_id  # Assuming subcategory_id has a category_id field
            if category:
                # Fetch all subcategories under the same category
                subcategories_in_category = request.env['product.subcategories'].sudo().search(
                    [('category_id', '=', category.id)]
                )

                for subcategory in subcategories_in_category:
                    subcategory_name = subcategory.name
                    if subcategory_name and subcategory_name not in unique_subcategories:
                        unique_subcategories.add(subcategory_name)
                        related_subcategories.append({'name': subcategory_name})
                    if len(unique_subcategories) >= 5:
                        break
            if len(unique_subcategories) >= 5:
                break

        total_pages = (total_buyers + per_page - 1) // per_page  # Calculate the total number of pages

        vals = {
            'suppliers': suppliers,
            'buyers': buyers,
            'query': product,
            'related_products': related_products,
            'related_subcategories': unique_subcategories,
            'supplier_search': False,
            'buyer_search': True,
            'page': page,
            'total_pages': total_pages,
            'partner':partner_id,
            'country_ids':country_ids,
            'logged_in':request.env.user != request.env.ref('base.public_user')
        }
        return request.render("trademeda.findSuppliers", vals)
    

    

    @http.route('/findSuppliersByCategory/<string:category>', method=['GET'], type='http', auth='public', website=True)
    def searchSupplierByCategory(self, category,country_ids=[], page=1, **kw):
        per_page = 20  # Number of suppliers per page
        offset = (int(page) - 1) * per_page  # Calculate the offset

        user = request.env.user
        partner_id = user.partner_id

        # Fetch the suppliers with pagination
        suppliers = request.env['product.customer.images'].sudo().search(
            [('product_id.subcategory_id.name', 'ilike', category)], limit=per_page, offset=offset)
        
        # Fetch the total count of suppliers for pagination calculation
        total_suppliers = request.env['product.customer.images'].sudo().search_count(
            [('product_id.subcategory_id.name', 'ilike', category)])
        
        # Calculate the total number of pages
        total_pages = math.ceil(total_suppliers / per_page)
        
        buyers = request.env['trademeda.rfq'].sudo().search(
            [('product_subsubcategory.subcategory_id.name', 'ilike', category)])

        # Fetch related subcategories
        related_subcategories = request.env['product.subcategories'].sudo().search(
            [('name', '=', category)]).category_id.subcategories_lines
        unique_subcategories = set()
        for rel_subcategory in related_subcategories:
            unique_subcategories.add(rel_subcategory.name)
            if len(unique_subcategories) >= 5:
                break
        subcategory = request.env['product.subcategories'].sudo().search([('name','ilike',category)],limit=1)
        points = subcategory.points + 10
        subcategory.sudo().write({
            'points':points
        })

        vals = {
            'suppliers': suppliers,
            'buyers': buyers,
            'query': category,
            'related_products': [],
            'related_subcategories': unique_subcategories,
            'supplier_search': True,
            'buyer_search': False,
            'page': page,
            'total_pages': total_pages,
            'searchByCategory':True,
            'partner':partner_id,
            'country_ids':country_ids,
            'logged_in':request.env.user != request.env.ref('base.public_user')
        }
        return request.render("trademeda.findSuppliers", vals)
    

    @http.route('/readytobuy', method=['GET'], type='http', auth='public', website=True)
    def searchAllReadyToBuyProduct(self,country_ids=[], page=1, **kw):
        per_page = 20  # Number of suppliers per page
        offset = (int(page) - 1) * per_page


        user = request.env.user
        partner_id = user.partner_id

        suppliers = request.env['product.customer.images'].sudo().search(
            [('ready_to_ship','=',True)],
            limit=per_page, offset=offset
        )
        total_suppliers = request.env['product.customer.images'].sudo().search_count(
            [('ready_to_ship','=',True)]
        )

        related_products = request.env['product.template'].sudo().search([], limit=10)
        unique_subcategories = set()
        related_subcategories = []

        for rel_product in related_products:
            category = rel_product.subcategory_id.category_id
            if category:
                subcategories_in_category = request.env['product.subcategories'].sudo().search(
                    [('category_id', '=', category.id)]
                )

                for subcategory in subcategories_in_category:
                    subcategory_name = subcategory.name
                    if subcategory_name and subcategory_name not in unique_subcategories:
                        unique_subcategories.add(subcategory_name)
                        related_subcategories.append({'name': subcategory_name})
                    if len(unique_subcategories) >= 5:
                        break
            if len(unique_subcategories) >= 5:
                break

        total_pages = (total_suppliers + per_page - 1) // per_page  # Calculate the total number of pages

        vals = {
            'suppliers': suppliers,
            'related_products': related_products,
            'related_subcategories': unique_subcategories,
            'supplier_search': True,
            'buyer_search': False,
            'page': page,
            'total_pages': total_pages,
            'country_ids':country_ids,
            'logged_in':request.env.user != request.env.ref('base.public_user'),
            'partner':partner_id
        }
        return request.render("trademeda.readyToBuy", vals)
    

    @http.route('/readytobuy/<string:product>', method=['GET'], type='http', auth='public', website=True)
    def searchReadyToBuyProduct(self,product,country_ids=[], page=1, **kw):
        per_page = 20  # Number of suppliers per page
        offset = (int(page) - 1) * per_page

        user = request.env.user
        partner_id = user.partner_id

        suppliers = request.env['product.customer.images'].sudo().search(
            [
                '&',
                ('ready_to_ship', '=', True),
                '|', '|',
                ('product_id.name', 'ilike', product),
                ('product_name', 'ilike', product),
                ('partner_id.name', 'ilike', product)
            ],
            limit=per_page, offset=offset
        )
        total_suppliers = request.env['product.customer.images'].sudo().search_count(
            [
                '&',
                ('ready_to_ship', '=', True),
                '|',
                ('product_id.name', 'ilike', product),
                ('product_name', 'ilike', product)
            ]
        )

        related_products = request.env['product.template'].sudo().search([('name', 'ilike', product)], limit=10)
        unique_subcategories = set()
        related_subcategories = []

        for rel_product in related_products:
            category = rel_product.subcategory_id.category_id
            if category:
                subcategories_in_category = request.env['product.subcategories'].sudo().search(
                    [('category_id', '=', category.id)]
                )

                for subcategory in subcategories_in_category:
                    subcategory_name = subcategory.name
                    if subcategory_name and subcategory_name not in unique_subcategories:
                        unique_subcategories.add(subcategory_name)
                        related_subcategories.append({'name': subcategory_name})
                    if len(unique_subcategories) >= 5:
                        break
            if len(unique_subcategories) >= 5:
                break

        total_pages = (total_suppliers + per_page - 1) // per_page  # Calculate the total number of pages

        vals = {
            'suppliers': suppliers,
            'related_products': related_products,
            'related_subcategories': unique_subcategories,
            'supplier_search': True,
            'buyer_search': False,
            'page': page,
            'total_pages': total_pages,
            'partner':partner_id,
            'country_ids':country_ids,
            'logged_in':request.env.user != request.env.ref('base.public_user')
        }
        return request.render("trademeda.readyToBuy", vals)
    


    @http.route('/newArrivals', method=['GET'], type='http', auth='public', website=True)
    def searchAllNewArrivals(self,country_ids=[], page=1, **kw):
        per_page = 20  # Number of suppliers per page
        offset = (int(page) - 1) * per_page

        user = request.env.user
        partner_id = user.partner_id

        suppliers = request.env['product.customer.images'].sudo().search(
            [],
            order='create_date desc',
            limit=per_page, offset=offset
        )
        buyers = request.env['trademeda.rfq'].sudo().search(
            [],order='create_date desc',limit=per_page, offset=offset)
        total_suppliers = request.env['product.customer.images'].sudo().search_count(
            []
        )
        rel = request.env['trademeda.rfq'].sudo().read_group(
                            domain=[('product_subsubcategory', '!=', False)],
                            fields=['product_subsubcategory', 'product_subsubcategory_count:count(product_subsubcategory)'],
                            groupby=['product_subsubcategory'],
                            orderby='product_subsubcategory_count desc')
        


        related_products = request.env['product.template'].sudo().search([], limit=10)
        unique_subcategories = set()
        related_subcategories = []

        for rel_product in related_products:
            category = rel_product.subcategory_id.category_id
            if category:
                subcategories_in_category = request.env['product.subcategories'].sudo().search(
                    [('category_id', '=', category.id)]
                )

                for subcategory in subcategories_in_category:
                    subcategory_name = subcategory.name
                    if subcategory_name and subcategory_name not in unique_subcategories:
                        unique_subcategories.add(subcategory_name)
                        related_subcategories.append({'name': subcategory_name})
                    if len(unique_subcategories) >= 5:
                        break
            if len(unique_subcategories) >= 5:
                break

        total_pages = (total_suppliers + per_page - 1) // per_page  # Calculate the total number of pages

        vals = {
            'suppliers': suppliers,
            'buyers': buyers,
            'related_products': related_products,
            'related_subcategories': unique_subcategories,
            'supplier_search': True,
            'buyer_search': False,
            'page': page,
            'total_pages': total_pages,
            'partner':partner_id,
            'country_ids':country_ids,
            'logged_in':request.env.user != request.env.ref('base.public_user')
        }
        return request.render("trademeda.findSuppliers", vals)
    

    @http.route('/featuredProducts', method=['GET'], type='http', auth='public', website=True)
    def searchfeaturedProducts(self,country_ids=[], page=1, **kw):
        per_page = 20  # Number of suppliers per page
        offset = (int(page) - 1) * per_page

        user = request.env.user
        partner_id = user.partner_id

        suppliers = request.env['product.customer.images'].sudo().search(
            [],
            order='views desc',
            limit=per_page, offset=offset
        )
        buyers = request.env['trademeda.rfq'].sudo().search(
            [],order='views desc',limit=per_page, offset=offset)
        total_suppliers = request.env['product.customer.images'].sudo().search_count(
            []
        )
        # rel = request.env['trademeda.rfq'].sudo().read_group(
        #                     domain=[('product_subsubcategory', '!=', False)],
        #                     fields=['product_subsubcategory', 'product_subsubcategory_count:count(product_subsubcategory)'],
        #                     groupby=['product_subsubcategory'],
        #                     orderby='product_subsubcategory_count desc')
        # import wdb;wdb.set_trace()


        related_products = request.env['product.template'].sudo().search([], limit=10)
        unique_subcategories = set()
        related_subcategories = []

        for rel_product in related_products:
            category = rel_product.subcategory_id.category_id
            if category:
                subcategories_in_category = request.env['product.subcategories'].sudo().search(
                    [('category_id', '=', category.id)]
                )

                for subcategory in subcategories_in_category:
                    subcategory_name = subcategory.name
                    if subcategory_name and subcategory_name not in unique_subcategories:
                        unique_subcategories.add(subcategory_name)
                        related_subcategories.append({'name': subcategory_name})
                    if len(unique_subcategories) >= 5:
                        break
            if len(unique_subcategories) >= 5:
                break

        total_pages = (total_suppliers + per_page - 1) // per_page  # Calculate the total number of pages

        vals = {
            'suppliers': suppliers,
            'buyers': buyers,
            'related_products': related_products,
            'related_subcategories': unique_subcategories,
            'supplier_search': True,
            'buyer_search': False,
            'page': page,
            'total_pages': total_pages,
            'partner':partner_id,
            'country_ids':country_ids,
            'logged_in':request.env.user != request.env.ref('base.public_user')
        }
        return request.render("trademeda.findSuppliers", vals)

    @http.route('/findBuyers/country/<int:country_id>', method=['GET'], type='http', auth='public', website=True)
    def searchBuyersByCountry(self,country_id,product="None", page=1, **kw):
        per_page = 20  # Number of suppliers per page
        offset = (int(page) - 1) * per_page
        # import wdb;wdb.set_trace()
        # print("Productt",product)

        user = request.env.user
        partner_id = user.partner_id
        # import wdb;wdb.set_trace()
        domain = [('partner_id.country_id.id', '=', country_id)]
        if product != "None":
            domain = ['|'] + domain + [('product_subsubcategory.name', 'ilike', product), ('product_name', 'ilike', product)]
        
        data = request.httprequest.get_json()
        if data:
            domain.append(('partner_id.country_id', 'in', data))

        total_buyers = request.env['trademeda.rfq'].sudo().search_count(domain)

        buyers = request.env['trademeda.rfq'].sudo().search(domain)

        related_products = request.env['product.template'].sudo().search([], limit=10)
        unique_subcategories = set()
        related_subcategories = []

        for rel_product in related_products:
            category = rel_product.subcategory_id.category_id
            if category:
                subcategories_in_category = request.env['product.subcategories'].sudo().search(
                    [('category_id', '=', category.id)]
                )

                for subcategory in subcategories_in_category:
                    subcategory_name = subcategory.name
                    if subcategory_name and subcategory_name not in unique_subcategories:
                        unique_subcategories.add(subcategory_name)
                        related_subcategories.append({'name': subcategory_name})
                    if len(unique_subcategories) >= 5:
                        break
            if len(unique_subcategories) >= 5:
                break

        total_pages = (total_buyers + per_page - 1) // per_page  # Calculate the total number of pages

        vals = {
            'buyers': buyers,
            'related_products': related_products,
            'related_subcategories': unique_subcategories,
            'supplier_search': True,
            'buyer_search': False,
            'page': page,
            'total_pages': total_pages,
            'partner':partner_id,
            'country_id':country_id,
            'logged_in': request.env.user != request.env.ref('base.public_user')
        }
        return request.render("trademeda.searchBuyersByCountry", vals)
    
    @http.route('/findSuppliers/country/<int:country_id>', method=['GET'], type='http', auth='public', website=True)
    def searchSuppliersByCountry(self,country_id,product="None", page=1, **kw):
        per_page = 20  # Number of suppliers per page
        offset = (int(page) - 1) * per_page

        user = request.env.user
        partner_id = user.partner_id
        # import wdb;wdb.set_trace()
        domain = [('partner_id.country_id.id','=',country_id)]
        if product != 'None':
             domain = ['|'] + domain + [('product_id.name', 'ilike', product), ('product_name', 'ilike', product)]
        
        
        data = request.httprequest.get_json()
        if data:
            domain.append(('partner_id.country_id', 'in', data))

        suppliers = request.env['product.customer.images'].sudo().search(domain, limit=per_page, offset=offset)
        total_suppliers = request.env['product.customer.images'].sudo().search_count(domain)


        related_products = request.env['product.template'].sudo().search([], limit=10)
        unique_subcategories = set()
        related_subcategories = []

        for rel_product in related_products:
            category = rel_product.subcategory_id.category_id
            if category:
                subcategories_in_category = request.env['product.subcategories'].sudo().search(
                    [('category_id', '=', category.id)]
                )

                for subcategory in subcategories_in_category:
                    subcategory_name = subcategory.name
                    if subcategory_name and subcategory_name not in unique_subcategories:
                        unique_subcategories.add(subcategory_name)
                        related_subcategories.append({'name': subcategory_name})
                    if len(unique_subcategories) >= 5:
                        break
            if len(unique_subcategories) >= 5:
                break

        total_pages = (total_suppliers + per_page - 1) // per_page  # Calculate the total number of pages

        vals = {
            'suppliers': suppliers,
            'related_products': related_products,
            'related_subcategories': unique_subcategories,
            'supplier_search': True,
            'buyer_search': False,
            'page': page,
            'total_pages': total_pages,
            'partner':partner_id,
            'country_id':country_id,
            'logged_in': request.env.user != request.env.ref('base.public_user')
        }
        return request.render("trademeda.searchSuppliersByCountry", vals)