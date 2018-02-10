from odoo import api, fields, models

class inherited_stock_pack_operation(models.Model):

    _inherit = 'stock.pack.operation'

    name = fields.Char()

    # @api.multi()
    # def do_new_transfer(self):
    #