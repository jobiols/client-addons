# For copyright and license notices, see __manifest__.py file in module root

from odoo import api, fields, models, _
from datetime import datetime
from dateutil import relativedelta

DATE_FORMAT = '%Y-%m-%d'


class SaleOrder(models.Model):
    _inherit = "sale.order"

    participant_ids = fields.One2many(
        'seguros_rest.participant',
        'sale_order_id',
        help="Travellers"
    )
    category_id = fields.Many2one(
        'product.category',
        help="Product Category"
    )
    departure_date = fields.Date(
        help="Trip start date"
    )
    return_date = fields.Date(
        help="Trip end date"
    )

    def simulate_quote(self):
        """ Simular un presupuesto manualmente
        """
        self.ensure_one()

        birth_dates = []
        # armar lista con las fechas de nacimiento
        for participant in self.participant_ids:
            birth_dates.append(participant.birth_date)

        self.select_products(birth_dates, self.departure_date,
                             self.return_date, self.category)

    @staticmethod
    def get_age(birth, today):
        """ obtener la edad al dia today """
        b_date = datetime.strptime(birth, DATE_FORMAT)
        t_date = datetime.strptime(today, DATE_FORMAT)
        return relativedelta.relativedelta(t_date, b_date).years

    def select_products(self, birth_dates, departure_date, return_date,
        category_id):
        """
        birth_dates: lista de fechas de nacimiento de los participantes
        departure_date: Fecha de inicio del viaje
        return_date: Fecha de finalizacion del viaje
        category: Categoria del seguro

        Selecciona de todos los productos, los que se les van a presentar al
        cliente y los deja cargados en el presupuesto con el precio calculado.
        """

        # obtener la fecha mas antigua de nacimiento de los participantes.
        birth_dates.sort()
        agest_birth_date = birth_dates[0]

        # obtener los dias de viaje incluidas ambas fechas
        d_date = datetime.strptime(departure_date, DATE_FORMAT)
        r_date = datetime.strptime(return_date, DATE_FORMAT)
        travel_days = (r_date - d_date).days + 1

        # obtener la edad del viajero mas viejo al dia de la fecha de regreso
        oldest_age = self.get_age(agest_birth_date, return_date)

        # buscar en product.template los productos a ofrecer para este conjunto
        # de participantes
        prod_tmpl = self.env['product.template']
        domain = [
            # Traer productos de esta categoria
            ('categ_id', '=', category_id),

            # Traer productos con destaque mayor que cero
            ('plano_destaque', '>', 0),

            # Traer productos si la edad limite del producto no es superado por
            # alguno de los participantes hasta la fecha de regreso inclusive
            ('limte_edad', '>=', oldest_age)
        ]

        products = prod_tmpl.search(domain)
        if not products:
            raise Warning(_('No products found to offer'))

        price = 0

        # procesar y salvar los productos en la SO
        for product in products:

            for birth in birth_dates:
                # edad del pasajero a la fecha de regreso
                age = self.get_age(birth, return_date)

                # determino si hay que incrementar el precio

                # si el producto tiene incremen en false o tiene limite de edad
                # en False no se incrementa
                if not product.increment or not product.limte_edad:
                    price += product.lst_price

                # si la edad del pasajero a la fecha del regreso es menor o
                # igual a la fecha de referencia, no se incrementa
                elif age < product.limte_edad:
                    price += product.lst_price

                # no cumple las anteriores, el pasajero tiene edad mayor que
                # la limite y tiene marcado incremento entonces se incrementa
                else:
                    price += product.lst_price * 1.5

                # ya tenemos el precio por dia ahora multiplicamos por la
                # cantidad de dias del viaje
                price *= travel_days

            vals = {
                'order_id': self.id,
                'product_id': product.id,
                'price_unit': price
            }
            # Crea la linea de presupuesto con este producto
            self.order_line.create(vals)
