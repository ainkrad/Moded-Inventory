from odoo import api, fields, models

class PaymentConfig(models.Model):
    _name = 'payment.config'

    name = fields.Char()

    less_perc = fields.Float(string='Percentage')

    bpt = fields.Boolean(string='isTerm',default=False)

    no_months = fields.Integer()

