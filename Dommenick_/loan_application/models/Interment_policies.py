from odoo import api, fields, models

class IntermentPol(models.Model):
    _name = 'interment.policy'

    name = fields.Text()
    active = fields.Boolean(default=True)
    is_parent = fields.Boolean(default=False)
    # policies_id = fields.Many2many(comodel_name="interment.policy", string="", )
    policies_id = fields.Many2one(comodel_name="interment.policy", string='policy', required=0)
                                  # compute="_get_policies"
    # policies_ids = fields.One2many(comodel_name="interment.policy", inverse_name="policies_id",  string="Policies", required=False,
    #                              domain=[('active','=',True)])
    policies_ids = fields.One2many(comodel_name="interment.policy", inverse_name="policies_id", string="", required=False,
                                   domain=[('is_parent','=',False)])


class printPolicy(models.TransientModel):
    _name = 'print.policy'

    name = fields.Many2one('res.partner', string='Names')
    dateDone = fields.Date(default=fields.Date.today(), string='Date Done')
    policy_id = fields.Many2one('interment.policy',string='Policy',domain=[('is_parent','=',True)])

    @api.multi
    def print_report(self):
        return{
            'type': 'ir.actions.report.xml',
            'report_name': 'loan_application.policy_report_view'
        }


