# For copyright and license notices, see __manifest__.py file in module root

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    participant_ids = fields.One2many(
        'seguros_rest.participant',
        'sale_order_id'
    )
    category = fields.Selection([
        ('general', 'Generals'),
        ('annuities', 'Annuities'),
        ('sports', 'Sports'),
        ('general', 'Generals'),
        ('long_stay', 'Long Stay'),
    ])
    departure_date = fields.Date(

    )
    return_date = fields.Date(

    )

    def simulate_quote(self):
        """ Simular un presupuesto manualmente
        """
        pass
