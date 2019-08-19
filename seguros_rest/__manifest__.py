##############################################################################
#
#    Copyright (C) 2019  jeo Software  (http://www.jeosoft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Seguros REST',
    'version': '11.0.0.0.0',
    'category': 'Tools',
    'summary': "Cotizador de seguros",
    'author': "jeo Software",
    'website': 'http://github.com/jobiols/client=addons',
    'license': 'AGPL-3',
    'depends': [
        'base_rest',
        'seguros_teste',
        'sale_management',
        'auth_api_key'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'views/sale_views.xml',
        'views/participant_view.xml'
    ],
    'demo': [

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
