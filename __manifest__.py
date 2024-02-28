# -*- coding: utf-8 -*-
{
    'name': 'Knjiznica',
    'version': '1.0',
    'summary': 'Knjiznica software',
    'sequence': 1,
    'description': """Knjiznica software""",
    'category': 'Productivity',
    'depends': ['mail', 'website_slides', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/knjiga.xml',
        'report/knjiga.xml',
        'report/report.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False
}
