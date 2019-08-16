# For copyright and license notices, see __manifest__.py file in module root

from odoo import api, fields, models, _


class Participant(models.Model):
    _name = "seguros_rest.participant"
    _description = "Travelers who are insured"
    _order = 'name'

    name = fields.Char(
        required=True
    )
    document = fields.Char(
        required=True
    )
    email = fields.Char(
        required=True
    )
    birth_date = fields.Date(
        required=True
    )
    sale_order_id = fields.Many2one(
        'sale.order',
        'Sales Order',
        required=True
    )
