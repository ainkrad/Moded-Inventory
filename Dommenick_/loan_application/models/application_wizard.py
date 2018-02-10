# from odoo import api, fields, models, _
#
#
# class CustomerWizard(models.Model):
#     _name = 'client.wizard'
#     _inherits = {'res.partner': 'partner_id'}
#
#     # name = fields.Char()
#     # suffix = fields.Selection(default='')
#
#     state = fields.Selection(selection=[('step1', 'General Information'),
#                                         ('step2', 'Billing Address'),
#                                         ('step3', 'STEP 3'),
#                                         ],
#                              required=False,
#                              default='step1'
#                              )
#
#     @api.multi
#     def action_next_1(self,cr,uid,ids,context=None):
#         # self.state = 'step1'
#         self.write(cr, uid, ids, {'state':'state2',}, context=context)
#         return{
#             'type': 'ir.actions.act_window',
#             'res_model': 'client.wizard',
#             'view_mode': 'form',
#             'view_type': 'form',
#             'res_id': self.id,
#             'view_id': self.env.ref('loan_application.client_wizard_form').id,
#             'target': 'new',
#         }
#
#     @api.multi
#     def action_next_2(self):
#         self.state = 'step2'
#
#     @api.multi
#     def action_next_3(self):
#         self.state = 'step3'
#
#
#     @api.onchange('first_name','middle_name','last_name','suffix')
#     def onchange_name(self):
#
#         name = ''
#         sep = ','
#         if self.last_name:
#             lname = self.last_name.title().strip()
#         else:
#             lname = ''
#         if lname:
#             name = '%s%s' % (lname, sep)
#
#         if self.first_name:
#             fname = self.first_name.title().strip()
#         else:
#             fname = ''
#         if fname:
#             name = '%s%s%s' % (name,' ',fname)
#
#         if self.suffix:
#             sfx = self.suffix.title().strip()
#         else:
#             sfx = ''
#         if sfx:
#             name = '%s%s%s' % (name,' ',sfx)
#
#         if self.middle_name:
#             mname = self.middle_name.title().strip()
#         else:
#             mname = ''
#         if mname:
#             name = '%s%s%s' % (name,' ',mname)
#
#         self.name = name
#         self.first_name = fname.title().strip()
#         self.middle_name = mname.title().strip()
#         self.last_name = lname.title().strip()
#         # self.suffix = sfx.strip()
#     #
#     # @api.multi
#     # def _get_suffix(self, values):
#     #     if values == 'jr':
#     #         suffix = 'Jr'
#     #
#     #     elif values == 'sr':
#     #         suffix = 'Sr'
#     #
#     #     elif values == 'ii':
#     #         suffix = 'II'
#     #
#     #     elif values == 'iii':
#     #         suffix = 'III'
#     #
#     #     elif values == 'iv':
#     #         suffix = 'IV'
#     #
#     #     elif values == 'v':
#     #         suffix = 'V'
#     #
#     #     elif values == 'vi':
#     #         suffix = 'VI'
#     #
#     #     elif values == 'vii':
#     #         suffix = 'VII'
#     #
#     #     else:
#     #         suffix = ''
#     #
#     #     return suffix
#     #
#     # @api.model
#     # def create(self, values):
#     #
#     #     if values['is_company'] == False:
#     #         fname = values['first_name']
#     #         mname = values['middle_name']
#     #         lname = values['last_name']
#     #         suffix_ids = values['suffix']
#     #         suffix = self._get_suffix(suffix_ids)
#     #         values['name'] = "%s, %s %s %s" % (lname, fname, suffix, mname)
#     #         values['first_name'] = fname
#     #         values['middle_name'] = mname
#     #         values['last_name'] = lname
#     #         values['suffix'] = suffix_ids
#     #     else:
#     #         g_name = values['name']
#     #         values['name'] = "%s" % (g_name)
#     #
#     #     rec = super(CustomerWizard, self).create(values)
#     #
#     #     return rec
#     #
#     # @api.multi
#     # def write(self, values):
#     #
#     #     rec = None
#     #
#     #     if 'parent_id' not in values:
#     #         if 'first_name' in values and values['first_name']:
#     #             fname = values['first_name'].title().strip()
#     #         elif 'first_name' not in values and self.first_name:
#     #             fname = self.first_name.title().strip()
#     #         else:
#     #             fname = ''
#     #
#     #         if 'middle_name' in values and values['middle_name']:
#     #             mname = values['middle_name'].title().strip()
#     #         elif 'middle_name' not in values and self.middle_name:
#     #             mname = self.middle_name.title().strip()
#     #         else:
#     #             mname = ''
#     #
#     #         if 'last_name' in values and values['last_name']:
#     #             lname = values['last_name'].title().strip()
#     #         elif 'last_name' not in values and self.last_name:
#     #             lname = self.last_name.title().strip()
#     #         else:
#     #             lname = ''
#     #
#     #         if 'suffix' in values and values['suffix']:
#     #             suffix = values['suffix']
#     #         elif 'suffix' not in values and self.suffix:
#     #             suffix = self.suffix
#     #         else:
#     #             suffix = ' '
#     #
#     #         if suffix:
#     #             suffix = self._get_suffix(suffix)
#     #
#     #         if 'first_name' in values and values['first_name'] or 'middle_name' in values and values[
#     #             'middle_name'] or 'last_name' in values and values['last_name']:
#     #             values['name'] = "%s, %s %s %s" % (lname, fname, suffix, mname)
#     #         else:
#     #             values['name'] = self.name
#     #
#     #         values['first_name'] = fname
#     #         values['middle_name'] = mname
#     #         values['last_name'] = lname
#     #     rec = super(CustomerWizard, self).create(values)
#     #     return rec
#     #
#     @api.multi
#     def copy(self, default=None):
#         self.ensure_one()
#         default = dict(default or {})
#         if ('name' not in default) and ('partner_id' not in default):
#             default['name'] = _("%s (copy)") % self.name
#             default['first_name'] = _("%s (copy)") % self.first_name
#             default['middle_name'] = _("%s (copy)") % self.middle_name
#             default['last_name'] = _("%s (copy)") % self.last_name
#             default['suffix'] = _("%s (copy)") % self.suffix
#         return super(CustomerWizard, self).copy(default)
#
#
