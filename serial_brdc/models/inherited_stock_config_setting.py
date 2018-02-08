from odoo import api, fields, models

class inherited_stock_config_setting(models.Model):

    _inherit = 'stock.config.settings'

    name = fields.Char()

