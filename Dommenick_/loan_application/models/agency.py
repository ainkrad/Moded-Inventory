from odoo import api, fields, models, exceptions

class ClientAgent(models.Model):
    _inherit = 'res.partner'

    agency_id = fields.Selection(string="Position", selection=[('am','Agency Manager'),
                                                               ('um','Unit Manager'),
                                                               ('sa','Sales Agent')], default='am')
    agent_manager_id = fields.Many2one('res.partner', string="Agency Manager",domain="[('is_agent','=',True),('agency_id','=','am')]", )
    unit_manager_id = fields.Many2one('res.partner', string="Unit Manager", domain="[('is_agent','=',True),('agency_id','=','um')]")
    sales_agent_id = fields.Many2one('res.partner', string="Sales Agent", domain="[('is_agent','=',True),('agency_id','=','sa')]")
    # domain = "[('','','')]"


    @api.onchange('unit_manager_id','agent_manager_id')
    # @api.multi
    def onchange_unit_manager(self):
        for sa in self.unit_manager_id:
            self.agent_manager_id = sa.agent_manager_id.id if sa.agent_manager_id else False

    @api.onchange('is_agent')
    def onchange_is_agent(self):
        self.agency_id = 'am'
        self.agent_manager_id = 0
        self.unit_manager_id = 0
        self.sales_agent_id = 0

    @api.onchange('agency_id')
    def onchange_position(self):
        self.agent_manager_id = 0
        self.unit_manager_id = 0
        self.sales_agent_id = 0

    @api.onchange('sales_agent_id','unit_manager_id','agent_manager_id')
    def onchange_sale_id(self):
        for sa in self.sales_agent_id:
            self.unit_manager_id = sa.unit_manager_id.id if sa.unit_manager_id else False
            self.agent_manager_id = sa.agent_manager_id.id if sa.agent_manager_id else False