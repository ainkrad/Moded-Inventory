from odoo import api, fields, models

class inherited_stock_quant(models.Model):

    _inherit = 'stock.quant'

    name = fields.Char()

    # status =