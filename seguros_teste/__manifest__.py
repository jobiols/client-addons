{
    'name': "Seguros Teste Oficial",
    'version': '1.0',
    'depends': ['website','website_form', 'website_partner', 'crm'],
    'data': [
        'views/seguros_view.xml',
        'data/data.xml',
        'views/extend_crm_lead.xml',
        ],
    'author': "Marcos V Mello",
    'category': 'Category',
    'description': """
    Description text
    """,
    'installable' : True,
}

#'security/ir.model.access.csv'