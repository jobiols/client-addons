# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

#    Forma de correr el test
#    -----------------------
#
#   Definir un subpackage tests que será inspeccionado automáticamente por
#   modulos de test los modulos de test deben enpezar con test_ y estar
#   declarados en el __init__.py, como en cualquier package.
#
#   Hay que crear una base de datos no importa el nombre pero se sugiere
#   [nombre cliente]_test_[nombre modulo] que debe estar vacia pero con el
#   modulo que se quiere testear instalado.
#
#   Debe tener usuario admin y password admin
#
#   Arrancar el test con:
#
#   oe -Q seguros_rest -c test11 -d test11_prod
#

from odoo.http import controllers_per_module

from .common import CommonCase
from ..controllers.main import BaseRestSeguroApiController


class TestController(CommonCase):

    def _check_default_routes(self, controller_cls, auth, root_path):
        for method_name in ('get', 'modify', 'update', 'delete'):
            method = getattr(controller_cls, method_name, None)
            self.assertIsNotNone(
                method,
                'Method %s is not declared on the controller %s' % (
                    method_name,
                    controller_cls
                ))
            routing = getattr(method, 'routing', None)
            # check that routes are defiend on method
            self.assertIsNotNone(
                routing,
                'No route defeined on method %s of controller %s' % (
                    method_name,
                    controller_cls
                )
            )
            # check the auth defined
            self.assertEqual(
                routing.get('auth'),
                auth,
                'Wrong auth defined on method %s' % method_name
            )
            # ensure that the route startswith the right root..
            routes = routing.get('routes', [])
            self.assertTrue(routes)
            for route in routes:
                self.assertTrue(
                    route.startswith(root_path),
                    'Route %s should start with %s' % (route, root_path)
                )

    def test_controller_registry(self):
        # at the end of the start process, our tow controllers must into the
        # controller registered

        import wdb;wdb.set_trace()

        controllers = controllers_per_module['seguros_rest']
        self.assertEqual(len(controllers), 2)

        self.assertIn(
            ('odoo.addons.base_rest_demo.controllers.main.'
             'BaseRestDemoPrivateApiController',
             BaseRestSeguroApiController),
            controllers
        )

    def test_controller_routes(self):
        # check that the generic routes are defined with the right url and auth
        self._check_default_routes(
            BaseRestSeguroApiController, auth="user",
            root_path="/insurance/v1/"
        )
