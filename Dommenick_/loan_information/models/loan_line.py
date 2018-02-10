from odoo import api, fields, models
from datetime import date, datetime,timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class IntermentLoanLine(models.Model):
    _name = 'interment.loan.line'
    _order = 'date_for_payment'

    @api.onchange('payment_id')
    def _get_payment_id(self):
        for rec in self:
            for res in rec.payment_id:
                rec.partner_id = res.partner_id.name if res.partner_id.name else False
                # rec.date_for_payment = res.payment_date if res.payment_date else False
                rec.paid_amount = res.amount if res.amount else False
                rec.balance = float(rec.paid_amount) - float(rec.amount_to_pay)
                rec.is_paid = (rec.payment_id != None)
                rec.update({'is_paid':rec.is_paid})
    
    display_name = fields.Char(related='payment_id.name')
    date_for_payment = fields.Date(string='Date of Payment', required=True, readonly=1)
    customer_id = fields.Many2one('res.partner', string='Customer', ondelete='cascade',readonly=1)
    amount_to_pay = fields.Float(string='Amount to Pay', required=True,readonly=1)
    is_paid = fields.Boolean(string='Paid', default=False,readonly=1,compute=_get_payment_id)
    notes = fields.Text()
    payment_term = fields.Many2one('payment.config', string='Payment Terms', domain=[('bpt','=',True)],readonly=1)
    loan_id = fields.Many2one('interment.quotation.request', string='Reference ID', ondelete='cascade',readonly=1)

    payment_id = fields.Many2one('account.payment',
                                 string='O.R. No',
                                 context={'default_payment_type': 'inbound', 'default_partner_type': 'customer'},
                                 domain=[('state','=','draft'),('partner_type', '=', 'customer')],
                                 # readonly=is_readonly
                                )

    partner_id = fields.Char(compute=_get_payment_id, string='Named To')
    paid_amount = fields.Float(string='Paid Amount',compute=_get_payment_id)
    balance = fields.Float(string="Customer's Balance",compute=_get_payment_id)
    state = fields.Selection([('draft','Draft'),('confirm','Confirm Payment')], default='draft')

    @api.multi
    def read_next_line(self):
        loan_line = self.env['interment.loan.line']
        for rec in self:
            date_start_str = datetime.strptime(rec.date_for_payment, '%Y-%m-%d')
            if rec.balance:
                date_start_str = date_start_str + relativedelta(months=1)
                next_line = loan_line.search([('date_for_payment','=', date_start_str)])
                next_line.update({'amount_to_pay': (next_line.amount_to_pay - rec.balance),
                                  'notes': str(rec.balance) + 'is Deducted on the amount to pay for this month.'
                                  })

        # pass

    @api.multi
    def draft_action(self):
        self.state = 'draft'

    @api.multi
    def confirm_action(self):
        self.state = 'confirm'
        self.read_next_line()

    @api.one
    def action_paid_amount(self):
        pass
    
class IntermentLoanLineDP(models.Model):
    _name = 'interment.loan.line.dp'
    _inherit = 'interment.loan.line'

