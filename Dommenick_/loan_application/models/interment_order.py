from odoo import api, fields, models, _, exceptions


class resPartner_IO(models.Model):
    _inherit = 'res.partner'

    interment_order_id = fields.One2many('interment.order','partner_id',string="Interment Order")
    is_deceased = fields.Boolean(default=False, string="Is Deceased")
    DateOfDeath = fields.Date(string='Date of Death',)
    CauseOfDeath = fields.Text(string='Cause of Date')



class IntermentOrder(models.Model):
    _name = 'interment.order'


    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       # states={'draft': [('readonly', False)]}, 
                       index=True, default=lambda self: _('New'))

    partner_id = fields.Many2one('res.partner', string='Customer', readonly=False, change_default=True, index=True, track_visibility='always',
                                 # ,compute="get_name",
                                # default = lambda self: self.env['res.partner'],
                                 )
    NatureOfInterment = fields.Selection([('fresh','Fresh'),('bone','Bone')], string='Nature Of Interment', default='fresh')
    # DateOfDeath = fields.Date(string='Date of Death',default=fields.Date.today())
    # CauseOfDeath = fields.Text(string='Cause of Date')
    song_ids = fields.One2many(comodel_name="song.request", inverse_name="interment_order_id", string="Requested Songs", required=False, limit=4)
    # states = {'draft': [('readonly', False)], 'sent': [('readonly', False)]},
    nature_selection = fields.Boolean(default = False)
    sale_id = fields.Many2one(comodel_name="sale.order", string="O.R. NO", required=False, )
    bone_transfer_ids = fields.Many2many('res.partner', string='name')
    informant_ids = fields.Many2one('res.partner', string='name')
    casket_size = fields.Selection([('standard','Standard'),('extra','Extra Large')], string='Casket Size')
    Wake_address = fields.Text()
    Lot_owner_id = fields.Many2one('res.partner', string="Lot Owner",)
    title_name = fields.Char(string='Title Name')
    # agent_id = fields.Char(string=)
    is_publish = fields.Boolean(default=False,string="Allow photos taken during interment published in MCEG FB Account")
    interment_datetime = fields.Datetime(string="Interment Date & Time")
    mass_datetime = fields.Datetime(string="Mass Date & Time")
    mass_location = fields.Text()

    @api.onchange('song_ids')
    def count_song_ids(self):
        for c in self:
            if len(c.song_ids) > 4:
                return{
                    'warning':{
                        'title':'Error',
                        'message':'Song request must be 4 only.'
                    }
                }

    
    
    @api.onchange('NatureOfInterment')
    def onchange_NatureOfInterment(self):
        self.nature_selection = (self.NatureOfInterment == 'bone')
        try:
            self.bone_transfer_ids = (5,self.bone_transfer_ids.ids)
        except:
            print "exception yeah"
        self.partner_id = None
        self.informant_ids = None
        
    @api.model
    def create(self, vals):
        if vals.get('name',_('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('interment.order') or _('')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('interment.order') or _('')
        # if vals.get('partner_id'):
        #     vals['partner_id'] = self.partner_id.id
        res = super(IntermentOrder, self).create(vals)
        return res

    @api.model
    def field_get_name(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        def get_name_id(xid, name):
            try:
                return self.env.ref('interment.' + xid)
            except ValueError:
                view = self.env['ir.ui.view'].search([('name','=',name)], limit=1)
                if not view:
                    return False
                return view.id

        context = self._context
        if context.get('active_model') == 'res.partner' and context.get('active_ids'):
            partner = self.env['res.partner'].browse(context['active_ids'])[0]
            if not view_type:
                view_id = get_name_id('interment_order_tree','interment.order.tree')
                view_type = 'tree'
            elif view_type == 'form':
                if partner.customer and not partner.supplier:
                    view_id = get_name_id('interment_order_form','interment.order.form').id

        return super(IntermentOrder, self).field_get_name(view_id=view_id,view_type=view_type, toolbar=toolbar, submenu=submenu)




class SongRequest(models.Model):
    _name = 'song.request'
    
    name = fields.Char(required=1, string='Requested Song')
    interment_order_id = fields.Many2one('interment.order',string='Interment Order')