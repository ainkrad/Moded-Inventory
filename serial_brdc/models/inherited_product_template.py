from odoo import api, fields, models


class inherited_product_template(models.Model):

    _inherit = 'product.template'

    name = fields.Char()

    tracking = fields.Selection(default='serial')

    list_price = fields.Float(default=0.00)

    area_number = fields.Char(string="Area")
    grave_type = fields.Char(string="Type")

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The Product already exist"),
    ]

    @api.onchange('categ_id')
    def set_type(self):
        self.grave_type = self.categ_id.name

    @api.depends('area_number', 'grave_type', 'categ_id')
    @api.onchange('area_number', 'grave_type', 'categ_id')
    def set_name(self):
        gt = self.grave_type
        if self.area_number and gt:
            self.name = "Area " + str(self.area_number) + " / " + str(gt)
            if ' ' in str(gt) or '-' in str(gt):
                if '-' in str(gt):
                    st = str(gt).split('-')
                else:
                    st = str(gt).split()
                at = ''
                for t in st:
                    at = at + t[0:1]
                self.default_code = "A" + str(self.area_number) + at
            else:
                self.default_code = "A" + str(self.area_number) + str(gt)[0:1]
        else:
            self.name = ""
            self.default_code = ""

            # @api.multi
            # def write(self, values):
            #     # Add code here
            #     # self.write()
            #     # values = {'default_code': self.default_code, 'grave_type': self.grave_type}
            #     return super(inherited_product_template, self).write(values)

            # @api.model
            # def create(self, values):
            #     # Add code here
            #     values = {'default_code': self.default_code,'grave_type':self.grave_type}
            #     return super(inherited_product_template, self).create(values)
            # class grave_type(models.Model):
            #
            #     _name = 'grave.type'
            #     _description = 'Grave type'
            #
            #     name = fields.Char()
