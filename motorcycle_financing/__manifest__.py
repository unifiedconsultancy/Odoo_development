{
    'name': 'Motorcycle Financing',
    'summary': 'Streamlines the loan application process for dealershops',
    'version': '18.0.0.0.1',
    'license': 'OPL-1',
    'category': 'Kawiil/Motorcycle',
    'author': 'Unified ERP Consultant',
    'depends': ['sale','product'],
    'data': [
        #security
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        #Views
        'views/loan_application_views.xml',
        'views/loan_setting_views.xml',
        'views/motorcycle_financing_menu.xml',
        'views/loan_tag_setting.xml',
        'views/loan_application_document_types.xml'
        #Menu
    ],
    'demo': [
        'demo/demo.xml'
    ],
    'application': 'True',
}
