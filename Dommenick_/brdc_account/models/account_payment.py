from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError

class AccountPayment(models.Model):
    # _name = 'loan.account.payment'
    _inherit = 'account.payment'
    _rec_name = 'or_series'




    user_id = fields.Many2one(comodel_name="res.users", string="Responsible", required=True,
                              default=lambda self: self.env.user, readonly=1)


    @api.model
    def create(self,vals):
        # if vals.get('or_series_text',_('New')) == _('New'):
        #     or_number_line = self.env['or.series.line']
        #     vals['or_series'] = or_number_line.search([('or_series_id.responsible','=', self.env.user.name),('state','=', 'unused')])[0].id
        #     vals['or_series_text'] = or_number_line.search([('id','=', vals['or_series'])]).name or _('New')
        # else:
        or_number_line = self.env['or.series.line']
        vals['or_series'] = or_number_line.search([('or_series_id.responsible', '=', self.env.user.name), ('state', '=', 'unused')])[0].id
        vals['or_series_text'] = or_number_line.search([('id', '=', vals['or_series'])]).name or _('New')
        vals['name'] = or_number_line.search([('id', '=', vals['or_series'])]).name
        # print self.or_series.state
        res = super(AccountPayment, self).create(vals)
        # write_status = self.or_series_write
        print self.or_series_write(vals['or_series_text'],'used')
        print self.payment_sequence_or_series(vals['or_series'],vals['or_series_text'])
        return res

    # @api.multi
    # def post(self):
    #     for rec in self:
    #         or_number_line = self.env['or.series.line']
    #         or_series = or_number_line.search([('or_series_id.responsible', '=', self.env.user.name), ('state', '=', 'unused')])[0].id
    #         rec.name = or_number_line.search([('id', '=', or_series)]).name
    #         rec.create({'name':rec.name})

    def get_default(self):
        or_number_line = self.env['or.series.line']
        return or_number_line.search([('or_series_id.responsible', '=', self.env.user.name), ('state', '=', 'unused')])[0].id


    def or_series_write(self,x,y):
        or_number_line = self.env['or.series.line']
        or_number = or_number_line.search([('name', '=', x)])
        rec = or_number.write({'state':y})
        return rec

    def payment_sequence_or_series(self,x,y):
        payment_line = self.env['account.payment']
        payments = payment_line.search([('or_series','=',x)])
        return payments.write({'name':y})

    @api.multi
    def post(self):
        for rec in self:

            if rec.state != 'draft':
                raise UserError(_("Only a draft payment can be posted. Trying to post a payment in state %s.") % rec.state)

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # Use the right sequence to set the name
            if rec.payment_type == 'transfer':
                sequence_code = 'account.payment.transfer'
            else:
                if rec.partner_type == 'customer':
                    if rec.payment_type == 'inbound':
                        sequence_code = 'account.payment.customer.invoice'
                    if rec.payment_type == 'outbound':
                        sequence_code = 'account.payment.customer.refund'
                if rec.partner_type == 'supplier':
                    if rec.payment_type == 'inbound':
                        sequence_code = 'account.payment.supplier.refund'
                    if rec.payment_type == 'outbound':
                        sequence_code = 'account.payment.supplier.invoice'
            rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
            if not rec.name and rec.payment_type != 'transfer':
                raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()

            rec.write({'state': 'posted', 'move_name': move.name})

        payment_line = self.env['account.payment']
        payments = payment_line.search([('or_series', '=', self.or_series.id)])
        return payments.write({'name': self.or_series.name})


    display_name= fields.Char(related='or_series.name')

    # or_series_text = fields.Char(string='OR No', required=True, readonly=True, copy=False,
    #                              default=lambda self: self.env['or.series.line'].search([('or_series_id.responsible','=', self.env.user.name),('state', '=', 'unused')])[0].name
    #                              )

    or_series = fields.Many2one('or.series.line',
                                string='O.R. Number',
                                readonly=1,
                                # domain=[('state','=','unused')],
                                default=lambda self: self.env['or.series.line'].search(
                                    [('or_series_id.responsible', '=', self.env.user.name), ('state', '=', 'unused')])[
                                    0].id
                                )


class ORSeriesConfiguration(models.Model):
    _name = 'or.series.config'

    name = fields.Char(related='reference_id')
    reference_id = fields.Char(string='Reference ID', required=True, readonly=True, copy=False, default=lambda self: _('New'))
    series_from = fields.Integer(string='Series From')
    series_to = fields.Integer(string='Series To')
    responsible = fields.Many2one('res.users',string='Assigned Personnel',required=True)
    or_series_line = fields.One2many(comodel_name="or.series.line", inverse_name="or_series_id", string="OR Series Line", required=True, index=True)
    state = fields.Selection([('draft','Draft'),('valid','Validated'),('confirm','Confirmed')], string='State', default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_valid(self):
        number = 1
        from_series = self.series_from
        for i in range(from_series, self.series_from + 1):
            start_series = 'O.R.-' + '%%0%sd' % 7 % from_series
            search_start_line = self.env['or.series.line'].search([('name', '=', start_series)])
            if search_start_line:
                raise UserError(_('Series is already existing'))
            else:
                self.state = 'valid'
            number += 1
            from_series = from_series + 1
        return True

    @api.multi
    def action_confirm(self):
        self.state = 'confirm'

    @api.multi
    def create_or_line(self):
        or_line = self.env['or.series.line']
        or_line.search([('or_series_id','=',self.id)]).unlink()
        for series in self:
            series.refresh()
            from_series = series.series_from

            number = 1
            for i in range(from_series, series.series_to + 1):
                line_id = or_line.create({
                    'name' : 'O.R.-' + '%%0%sd' % 7 % from_series,
                    'or_series_id': series.id,
                    'responsible': series.responsible.id,
                    'state': 'unused'
                })
                number += 1
                from_series = from_series + 1
        return True

    @api.model
    def create(self,vals):
        if vals.get('reference_id',_('New')) == _('New'):
            vals['reference_id'] = self.env['ir.sequence'].next_by_code('or.series.config') or _('New')

        return super(ORSeriesConfiguration, self).create(vals)




class ORSeriesLine(models.Model):
    _name = 'or.series.line'
    _order = 'state, name'

    name = fields.Char(string='OR Series', required=True, readonly= True)
    or_series_id = fields.Many2one(comodel_name="or.series.config", string="", required=False,readonly= True )
    responsible = fields.Many2one('res.users', string='Assigned Personnel', required=True)
    state = fields.Selection([('used','USED'),('unused','UNUSED')],readonly= True)

    # @api.model
    # def func_write(self,or_number):
    #     for i in self:
    #         if i.name == or_number:
    #             i.write({'state': 'used'})
    #

    @api.multi
    def or_series_write(self):
        for rec in self:
            or_number_line = self.env['or.series.line']
            or_number = or_number_line.search([('name', '=', rec.name)])
            if or_number:
                rec.write({'state': 'used'})