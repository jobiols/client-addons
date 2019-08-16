from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm


class MyFristModel(http.Controller):

    @http.route('/home',auth='public')
    def home(self,**kw):
        return 'hello from Tutorial Odoo 11 qweb'

class PlanosList(http.Controller):
    @http.route('/planos', auth='public', website=True) 
    def show_cobertura_data(self, **kw):
        plano = http.request.env['product.template'].sudo().search([])
        return http.request.render('seguros_teste.planos_details',{
            'plano': plano
            })
