# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest.controllers import main


class BaseRestSeguroApiController(main.RestController):
    _root_path = '/insurance/v1/'
    _collection_name = 'base.rest.insurance.services'
    _default_auth = 'user'
