{
    'name': 'Trademeda',
    'version': '1.0',
    'summary': '',
    'description': '',
    'author': 'eSehat Meditech Ltd',
    'license': 'LGPL-3',
    'category': 'Category',
    'depends': ['base','stock','contacts'],  # List your dependencies here
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',

        'views/product_category.xml',
        'views/menuitems.xml',
        'views/customer_inherited.xml',
        'views/product_inherited.xml',

        
        'views/portal/header.xml',
        'views/portal/homepage.xml',
        'views/portal/signup.xml',
        'views/portal/signin.xml',
        'views/portal/user_profile.xml',
        'views/portal/product_details.xml',
        'views/portal/supplier_profile.xml',
        'views/portal/wishlist.xml',



    ],
    'demo': [
        # 'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
}