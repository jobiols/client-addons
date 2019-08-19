# Copyright 2019 jeosoft.com.ar

from odoo.addons.component.core import Component
from odoo.exceptions import ValidationError
from odoo import _
from datetime import datetime


class QuotationService(Component):
    _inherit = 'base.rest.service'
    _name = 'quotation.service'
    _usage = 'quotation'
    _collection = 'base.rest.insurance.services'
    _description = """
        Quotation Service\n

        Access to the quotation service is autenticated by api_key
    """

    # pylint:disable=method-required-super
    def create(self, **params):
        """
        Create a new quotation
        """
        try:
            # chequear consistencia de parametros
            self._check_parameters(params)

            # convertir lead a cliente
            partner_id = self._convert_lead(params['lead_id']).id

            # crear el presupuesto
            vals = {
                'partner_id': partner_id,
                'category_id': params['category_id'],
                'departure_date': params['departure_date'],
                'return_date': params['return_date'],
            }
            q = self.env['sale.order'].create(vals)

            # crear los productos a ofrecer
            quotation = q.select_products(params['birth_dates'],
                                          params['departure_date'],
                                          params['return_date'],
                                          params['category_id'],
                                          throw_exceptions=False)

            # devolver los productos en la respuesta
            return self._quotation_to_json(quotation)

        except ValidationError as ex:
            # manejar las excepciones en validacion de datos.
            return self._validation_error(ex.name)

    # The following methods are 'private' and should be never never NEVER call
    # from the controller.

    @staticmethod
    def _lead_to_json(lead):
        """ Validar todos los parametros y devolver un json para crear el
            cliente
        """
        error = 'The field %s from the model crm.lead id=%d is empty'
        name = lead.contact_name
        if not name:
            raise ValidationError(_(error) % ('contact_name', lead.id))

        email = lead.email_from
        if not email:
            raise ValidationError(_(error) % ('email_from', lead.id))

        phone = lead.phone
        if not phone:
            raise ValidationError(_(error) % ('phone', lead.id))

        return {
            'name': name,
            'email': email,
            'phone': phone
        }

    def _convert_lead(self, lead_id):
        """ Crear el cliente a partir del lead
        """
        lead = self.env['crm.lead'].search([('id', '=', lead_id)])
        if not lead:
            raise ValidationError(_('The lead_id with id=%d is not found in '
                                    'the model crm.lead') % lead_id)

        # traducir el lead a json y crear el cliente
        vals = self._lead_to_json(lead)
        return self.env['res.partner'].create(vals)

    # Validators
    @staticmethod
    def _validator_create():
        """ Validator para los parametros de entrada
        """
        res = {
            'lead_id': {
                'type': 'integer',
                'required': True,
                'empty': False
            },
            'category_id': {
                'type': 'integer',
                'required': True,
                'empty': False
            },
            'departure_date': {
                'type': 'string',
                'nullable': False
            },
            'return_date': {
                'type': 'string',
                'required': True,
                'empty': False
            },
            'birth_dates': {
                'type': 'list',
                'required': True,
                'empty': False,
                'schema': {
                    'type': 'string'
                }
            }
        }
        return res

    @staticmethod
    def _validator_return_create():
        """ Validar los parametros de salida
        """
        res = {
            'partner_id': {
                'type': 'integer',
                'required': True,
                'empty': False
            },
            'quotation_id': {
                'type': 'integer',
                'required': True,
                'empty': False
            },
            'products': {
                'type': 'list',
                'required': True,
                'empty': True,
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'product_id': {
                            'type': 'integer',
                            'required': True,
                            'empty': False,
                        },
                        'price': {
                            'type': 'float',
                            'required': True,
                            'empty': False,
                        },
                        'description': {
                            'type': 'string',
                            'required': True,
                            'empty': False,
                        },
                        'long_description': {
                            'type': 'string',
                            'required': False,
                            'empty': False,
                        }
                    }
                }
            }
        }
        return res

    @staticmethod
    def _quotation_to_json(quotation):
        """ Transformar la quotation recien creada en la respuesta
        """
        #import wdb;wdb.set_trace()

        res = dict()
        res['partner_id'] = quotation.partner_id.id
        res['quotation_id'] = quotation.id
        res['products'] = []
        for sol in quotation.order_line:
            prod = dict()
            prod['product_id'] = sol.product_id.id
            prod['description'] = sol.product_id.name
            prod['price'] = sol.price_unit
            if sol.product_id.description:
                prod['long_description'] = sol.product_id.description
            res['products'].append(prod)
        return res

    @staticmethod
    def _validation_error(msg):
        raise ValidationError(msg)

    @staticmethod
    def _validator_return_validation_error():
        return {}

    @staticmethod
    def _validate_date(date):
        """ validar el formato de fecha, si esta mal levanta una excepcion
        """
        datetime.strptime(date, '%Y-%m-%d')

    def _check_parameters(self, params):
        """ Chequear consistencia de los parametros
        """
        category_id = params.get('category_id')
        departure_date = params.get('departure_date')
        return_date = params.get('return_date')
        birth_dates = params.get('birth_dates')

        category_obj = self.env['product.category']
        if not category_obj.search([('id', '=', category_id)]):
            raise ValidationError(_('The category_id=%d is not found in the '
                                    'product.category model') % category_id)
        try:
            txt = 'departure_date'
            self._validate_date(departure_date)
            data = departure_date

            txt = 'return_date'
            self._validate_date(return_date)
            data = return_date

            txt = 'birth_dates'
            for date in birth_dates:
                data = date
                self._validate_date(date)
        except ValueError as ex:
            raise ValidationError(
                _('Incorrect data format found on %s (%s). Error found: %s, '
                  'the format should be YYYY-MM-DD') % (txt, data, ex.args[0]))

        if departure_date > return_date:
            raise ValidationError(
                _('Departure date (%s) is grater than return date (%s)') % (
                    departure_date, return_date))
