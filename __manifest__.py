{
    'name': 'Trademeda',
    'version': '1.0',
    'summary': '',
    'description': '',
    'author': 'eSehat Meditech Ltd',
    'category': 'Category',
    'depends': ['base','stock'],  # List your dependencies here
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',

        'views/product_category.xml',
        'views/menuitems.xml',
        'views/portal/homepage.xml',
        'views/portal/signup.xml',
        'views/portal/signin.xml',
        'views/portal/product_details.xml',




    ],
    'demo': [
        # 'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
}