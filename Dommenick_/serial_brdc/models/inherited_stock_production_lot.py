from odoo import api, fields, models

class inherited_stock_production_lot(models.Model):

    _inherit = 'stock.production.lot'

    name = fields.Char(string="Lot Name / Niche Name")

    stat = [('av', 'Available'),
            ('fp', 'Fully Paid'),
            ('amo', 'Amortized'),
            ('wit', 'Interred'),
            ('r', 'Reserved'), ]

    block_number = fields.Char(string="Block Number / Layer")
    lot_number = fields.Char(string="Lot Number / Column")
    status = fields.Selection(stat, string="Status", default='av', readonly=False)
    interred_person = fields.One2many('res.partner', 'name', limit=2)

    product_qty = fields.Float(default=1)

    @api.depends('product_id')
    @api.onchange('product_id', 'block_number', 'lot_number')
    def set_lot_ser(self):
        if self.product_id and self.block_number and self.lot_number:
            if self.product_id.grave_type != 'Community Vault' or self.product_id.grave_type != 'Columbarium':
                self.ref = "A" + str(self.product_id.area_number) + "B" + str(self.block_number) + "L" + str(
                    self.lot_number)
                self.name = "A" + str(self.product_id.area_number) + "B" + str(self.block_number) + "L" + str(
                    self.lot_number)
            else:
                self.ref = "A" + str(self.product_id.area_number) + "L" + str(self.block_number) + "C" + str(
                    self.lot_number)
                self.name = "A" + str(self.product_id.area_number) + "L" + str(self.block_number) + "C" + str(
                    self.lot_number)
        else:
            self.ref = ""
            self.name = ""

class interred_person(models.Model):
    _model = 'interred.person'

    name = fields.Char()


