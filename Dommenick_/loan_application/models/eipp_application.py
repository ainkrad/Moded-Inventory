from odoo import api, fields, models, _

class eippApplication(models.Model):
    _name = 'eipp.application'

    refNo = fields.Char(required=True, copy=False, readonly=True, default=lambda self: _('New'), string='Reference Number')
    name = fields.Many2one('res.partner',domain=[('customer','=',True),('is_deceased','=',False)], string='Applicant Name')
    applicant_name = fields.Char()
    pa_no = fields.Char(compute='_get_pano')

    active = fields.Boolean(default = True)

    eipp_payment_plan = fields.Selection([('week_d','Weekdays'),
                                  ('week_e','Week End')], string='EIPP Plan Applied')
    eipp_amount_payment = fields.Float(string='Amount')

    or_id = fields.Many2one('sale.order',string='O.R. No')

    user_evaluate = fields.Many2one(comodel_name="res.users",
                                    string="Evaluated by",
                                    readonly=1,
                                    )
    user_approve = fields.Many2one(comodel_name="res.users",
                                   string="Approved by",
                                   readonly=1,
                                   )
    user_note = fields.Many2one(comodel_name="res.users",
                                string="Noted by",
                                readonly=1,
                                )

    state = fields.Selection([
        ('draft', "Draft"),
        ('eval', "Evaluated"),
        ('apro', "Approved"),
        ('note', 'Noted'),
    ], default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_eval(self):
        self.state = 'eval'
        self.user_evaluate = self.env.user

    @api.multi
    def action_apro(self):
        self.state = 'apro'
        self.user_approve = self.env.user

    @api.multi
    def action_note(self):
        self.state = 'note'
        self.user_note = self.env.user



    # @api.onchange('name')
    # def _get_pano(self):
    #     for s in self:
    #         for a in s.name:
    #             s.pa_no = a.ClientNo
    #             s.applicant_name = a.name
    #             print s.applicant_name


    @api.model
    def create(self,vals):
        if vals.get('refNo',_('New')) == _('New'):
            vals['refNo'] = self.env['ir.sequence'].next_by_code('eipp.application') or _('New')

            res = super(eippApplication, self).create(vals)
            return res




