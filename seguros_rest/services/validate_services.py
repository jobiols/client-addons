# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from odoo.addons.component.core import Component
from odoo.exceptions import ValidationError
from odoo import _
from datetime import datetime
from odoo.tools import config
import logging

_logger = logging.getLogger(__name__)


class ValidateService(Component):
    _inherit = 'base.rest.service'
    _name = 'validating.service'
    _usage = 'validate'
    _collection = 'base.rest.insurance.services'
    _description = """
        Validate Service\n

        Validate a previous created quotation
    """

    def update(self, _id, **params):
        """
        Validate quotation
        """
        try:
            # chequear consistencia de parametros
            self._check_parameters(params)

            # eliminar productos que no se han elegido
            quotation = self.env['sale.order'].search([('id', '=', _id)])
            product_id = params['product_id']
            participants = params['participants']

            if not quotation:
                msg = 'The quotation being validated (id=%d) does not exist.'
                raise ValidationError(_(msg) % _id)

            # verificar que el producto elegido exista en la cotizacion
            prod = quotation.order_line.filtered(
                lambda x: x.product_id.id == product_id)

            if not prod:
                msg = 'The product (id=%d) does not exist in the quotation '
                msg += '(id=%d) being validated.'
                raise ValidationError(_(msg) % (product_id, _id))

            # eliminar los que no eligieron
            for sol in quotation.order_line:
                if sol.product_id.id != product_id:
                    sol.unlink()

            # agregar los usuarios como seguidores
            self._set_users_to_notify(quotation)

            # validar el presupuesto
            quotation.action_confirm()

            # agregar los participantes
            for participant in participants:
                participant['sale_order_id'] = _id
                quotation.participant_ids.create(participant)

            return {'code': 200, 'description': 'OK'}

        except ValidationError as ex:
            # manejar las excepciones en validacion de datos.
            return self._validation_error(ex.name)

    @staticmethod
    def _validator_update():
        res = {
            'product_id': {
                'type': 'integer',
                'required': True,
                'empty': False
            },
            'participants': {
                'type': 'list',
                'required': True,
                'empty': False,
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'name': {
                            'type': 'string',
                            'required': True,
                            'empty': False
                        },
                        'document': {
                            'type': 'string',
                            'required': True,
                            'empty': False
                        },
                        'email': {
                            'type': 'string',
                            'required': True,
                            'empty': False
                        },
                        'birth_date': {
                            'type': 'string',
                            'required': True,
                            'empty': False
                        }
                    }

                }
            },
        }
        return res

    @staticmethod
    def _validator_return_update():
        res = {
            'code': {
                'type': 'integer',
                'required': True,
                'empty': False
            },
            'description': {
                'type': 'string',
                'required': True,
                'empty': False
            }
        }
        return res

    def _check_parameters(self, params):
        """ Chequea que las fechas de nacimiento esten escritas correctamente
        """
        for participant in params['participants']:
            try:
                datetime.strptime(participant['birth_date'], '%Y-%m-%d')
            except ValueError as ex:
                raise ValidationError(
                    _('Incorrect data format found on birth day of '
                      'participant %s. Error found: %s, the format should be '
                      'YYYY-MM-DD') % (participant['name'], ex.args[0]))

    @staticmethod
    def _validation_error(msg):
        raise ValidationError(msg)

    def _set_users_to_notify(self, order):
        """ Trae los usuarios definidos en el config y los agrega como
            seguidores en la orden de venta
        """
        users = config.get('users_to_notify')
        if not users:
            raise ValidationError(
                _('There are no users to notify, please add the list of users '
                  'to notify to your odoo.conf.<br> This way: '
                  '<strong>users_to_notify = user1,user2,user3<strong>')
            )
        users = users.replace(' ', '')
        users = users.split(',')
        for user in users:
            uid = self.env['res.users'].search([('login', '=', user)]).id
            if not uid:
                raise ValidationError(
                    _('There is no %s user on this system.<br> Please make '
                      'sure the user login is listed in the "users_to_notify" '
                      'option found in your odoo.conf') % user)
            order.message_subscribe_users(uid)
