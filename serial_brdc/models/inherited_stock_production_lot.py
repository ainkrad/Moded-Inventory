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
    loanee_id = fields.Char(default=" ")
    loanee_name = fields.Char(string="Loanee", default=" ", store=False)
    loanee_payment_term = fields.Char(string="Payment Term", default=" ", store=False)
    loanee_contract_price = fields.Char(string="Contract Price", default=" ", store=False)

    interred_person = fields.One2many('res.partner', 'name')

    product_qty = fields.Float(default=1)

    # @api.depends('product_id')
    # def set_loanee_info(self):
    #     # if self.env['stock.production.lot'].search([('id','=',self.id)]) != " ":
    #     print self.env['stock.production.lot'].search([('id','=',self.id)])

    @api.depends('product_id')
    @api.onchange('product_id', 'block_number', 'lot_number')
    def set_lot_ser(self):
        if self.product_id and self.block_number and self.lot_number:
            if self.product_id.grave_type != 'Community Vault' or self.product_id.grave_type != 'Columbarium':
                gt = self.product_id.grave_type
                if ' ' in str(gt):
                    st = str(gt).split()
                    at = ''
                    for t in st:
                        at = at + t[0:1]
                    self.ref = "A" + str(self.product_id.area_number) + "B" + str(self.block_number) + "L" + str(
                        self.lot_number) + at
                    self.name = "A" + str(self.product_id.area_number) + "B" + str(self.block_number) + "L" + str(
                        self.lot_number) + at
                else:
                    self.ref = "A" + str(self.product_id.area_number) + "B" + str(self.block_number) + "L" + str(
                        self.lot_number) + str(self.product_id.grave_type)[0:1]
                    self.name = "A" + str(self.product_id.area_number) + "B" + str(self.block_number) + "L" + str(
                        self.lot_number) + str(self.product_id.grave_type)[0:1]
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


