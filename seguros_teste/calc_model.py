from odoo import api, fields, models

class TestChamada(models.Model):
    _name = 'test.chamada'
    _description = 'Chamada para botao'

    def test_chamada(self):
        return 2
