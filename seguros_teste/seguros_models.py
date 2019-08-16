# solucion seguros app
from odoo import models, fields, api, exceptions
from datetime import datetime

# from datetime import datetime


class Coberturas_product_template(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    acc_enfer = fields.Float(string="Acc.y.Enfer",)
    preex = fields.Float(string="Preex",)
    min_dias = fields.Integer(string='Min.Días',)
    max_dias = fields.Integer(string="Máx.Días",)
    limte_edad = fields.Integer(string="Limite edad",)
    incremen = fields.Boolean(string="Incremen.%50",)
    ref_edad =  fields.Integer(string="Edad.Referen",)
    precio_per_dia = fields.Float(string="Precio venta x día",)
    costo_neto = fields.Float(string="Costo Neto",)
    plano_destaque = fields.Integer(string="Posicion Destaque",)

    @api.constrains('_plano_destaque' )
    def check_plano_destaque(self):
            if self._plano_destaque > 4:
                raise exceptions.ValidationError(
                    "O valor não pode ser maior que 4."
                )

class add_fields_crm_lead(models.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'

    rut = fields.Integer(string="RUT",)
    cedula = fields.Integer(string="Cédula",)


class infos_consulta(models.Model):
    _name = 'info.consulta'

    data_ida = fields.Datetime(string="Data de Ida",)
    data_volta = fields.Datetime(string="Data da volta",)
    num_pasageiros = fields.Integer(string="Número de Passageiros",)
    num_menores = fields.Integer(string="Menores de idade",)
    num_idosos = fields.Integer(string="Idosos",)
    esportes =  fields.Boolean(string="Praticará esportes?",)
    moto =  fields.Boolean(string="Utilizará motocicleta?",)
    total_dias = fields.Integer(string="Total de Dias", store=True, compute="calcula_dias",)

    @api.onchange('data_ida', 'data_volta','total_dias')
    def calcula_dias(self):
        if self.data_ida and self.data_volta:
            d1=datetime.strptime(str(self.data_ida),'%Y-%m-%d') 
            d2=datetime.strptime(str(self.data_volta),'%Y-%m-%d')
            d3=d2-d1
            self.total_dias=str(d3.days)

