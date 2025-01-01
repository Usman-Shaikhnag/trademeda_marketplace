{
    'name': 'Trademeda',
    'version': '1.0',
    'summary': '',
    'description': '',
    'author': 'eSehat Meditech Ltd',
    'license': 'LGPL-3',
    'category': 'Category',
    'depends': ['base','web','stock','contacts'],  # List your dependencies here
    'data': [
        'data/sequence_data.xml',
        'data/ir_cron.xml',

        'security/groups.xml',
        'security/ir.model.access.csv',

        'views/product_category.xml',
        'views/menuitems.xml',
        'views/awards_certificates.xml',
        'views/customer_inherited.xml',
        'views/product_inherited.xml',
        'views/country_inherited.xml',
        'views/rfq.xml',
        'views/customer_rating.xml',
        'views/quotation.xml',
        'views/pricing_plans.xml',
        'views/faqs.xml',
        'views/brochure_view.xml',
        'views/trademeda_emails.xml',


        
        'views/portal/header.xml',
        'views/portal/footer.xml',
        'views/portal/homepage.xml',
        'views/portal/signup.xml',
        'views/portal/signin.xml',
        'views/portal/user_profile.xml',
        'views/portal/product_details.xml',
        'views/portal/supplier_profile.xml',
        'views/portal/wishlist.xml',
        'views/portal/post_rfq.xml',
        'views/portal/quotation_details.xml',
        'views/portal/search.xml',
        'views/portal/categories.xml',
        'views/portal/subcategories.xml',
        'views/portal/readyToBuyProducts.xml',
        'views/portal/searchByCountry.xml',
        'views/portal/banner_application.xml',
        'views/portal/privacy_policy.xml',
        'views/portal/membership_plans.xml',
        'views/portal/countries.xml',
        'views/portal/brochure.xml',
        'views/portal/about_us.xml',
        'views/portal/testimony_application.xml',
        'views/portal/terms_and_condition.xml',
        'views/portal/product_listing_policy.xml',
        'views/portal/mission.xml',
        'views/portal/trust_score.xml',
        'views/portal/faq.xml'






    ],
    'demo': [
        # 'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,

    'assets': {
        'web.assets_frontend': [
            # 'trademeda/static/src/js/filter2.js',
            # 'trademeda/static/src/legacy/js/public/filters.js',
            # 'trademeda/static/**/*',

        ],
    },
}