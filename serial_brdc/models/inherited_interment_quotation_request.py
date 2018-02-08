from odoo import api, fields, models

class inherited_interment_quotation_request(models.Model):

    _inherit = 'interment.quotation.request'

    name = fields.Char()

    ls_number = fields.Many2one('stock.production.lot', string="Lot / Niche Name")

