from odoo import models, fields, api, exceptions, _ , tools
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class client(models.Model):
    # _name = 'res.partner'
    _inherit = 'res.partner'
    # _name = "res.partner_"

    _defaults = {
        'country_id': lambda self,cr, uid, context: self.pool.get('res.country').browse(cr,
                                                                                        uid,
                                                                                        self.pool.get('res.country').search(cr,
                                                                                                                            uid,
                                                                                                                            [('name','=','Philippines')]))[0].id,
    }
    
    # name = fields.Char(string="Name")
    first_name = fields.Char(string="First Name")
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name")
    suffix = fields.Selection([('jr', 'Jr'),
                               ('sr', 'Sr'),
                               ('iii', 'III'),
                               ('v', 'V'),
                               ('vi', 'VI'),
                               ('vii', 'VII')], string='Suffix')
    birthdate = fields.Date(string="Birth Date")

    age = fields.Char(string='age', store = False, compute='_get_age')
    
    # country_id = fields.Many2one('res.country', string='Country', change_default=True, default="_get_default_country")
    # region_id = fields.Many2one('config.region', string="Region")
    province_id = fields.Many2one('config.province', string="Province")
    municipality_id = fields.Many2one('config.municipality', string="Municipality",domain="[('province_id','=',province_id)]")
    barangay_id = fields.Many2one('config.barangay', string="Barangay",domain="[('municipality_id','=',municipality_id)]")

    # mothermaiden = fields.Char(string="Mother's Maiden Name", required=True)

    gender = fields.Selection([('male','Male'),
                               ('female','Female'),
                               ('other','Other')], string='Gender')
    weight = fields.Float(string='Weight (kg)')
    height = fields.Float(string='Height (cm)')
    religion_id = fields.Many2one('client.religion', string="Religion")
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced'),
        ('singleparent', "Single Parent"), 
        ('separated', 'Separated')
    ], string='Marital Status')

    type = fields.Selection(
        [('other', 'Other Address'),
         ('contact', 'Contact'),
         ('invoice', 'Invoice address'),
         ('delivery', 'Shipping address'),
         ], string='Address Type',
        default='contact',
        help="Used to select automatically the right address according to the context in sales and purchases documents.")

    # ClientNo = fields.Char(string="Client No",index=True, default=lambda self: _('New'),required=1,readonly=1)
    TIN = fields.Char(string="TIN")
    nationality_id = fields.Many2one("res.country", "Nationality (Country)")
    attainment = fields.Selection([('s1',"high school diploma or equivalency certificate"),
                                   ('s2',"an associate's degree"),
                                   ('s3',"a bachelor's degree"),
                                   ('s4',"a master's degree or higher degree")], string="Educational Attainment")
    yearGrad = fields.Char(string="Year Graduated")
    schoolGrad = fields.Text(string="School Graduated")
    
    ctcno = fields.Char(string="CTC Number")
    ctcpi = fields.Text(string="CTC Place Issued")
    ctcd = fields.Date(string="CTC Date")
    # user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    user_id = fields.Many2one(comodel_name="res.users", string="Responsible", required=True,
                                     default=lambda self: self.env.user, readonly=1)
    company = fields.Char(default='company')

    company_name_id = fields.Many2one('res.company',string="Company")
    
    street = fields.Text(string='Home')
    
    is_agent = fields.Boolean(string="Is Agent", default=False )

    position = fields.Char(string='Position')
    monthly_income = fields.Float(string='Monthly Income')
    employment_state_1 = fields.Selection(string="Employment Status",
                                         selection=[('employed', 'Employed'), 
                                                    ('self-employed', 'Self-employed'),
                                                    ('unemployed', 'Unemployed'),
                                                    ('other','Other(OFW)')],
                                         default='unemployed',
                                         required=False, )
    is_employed = fields.Boolean(default=False)
    employment_state = fields.Selection(string="Employment State",
                                        selection=[('regular', 'Regular'), 
                                                   ('contractual', 'Contractual'),
                                                   ('others','Others(Pls. Specify)') ],
                                        # compute='_compute_employment_state',
                                        # inverse='_write_employment_state',
                                        required=False, )
    is_others = fields.Boolean(default = False)
    if_others = fields.Text()
    
    is_unemployed = fields.Boolean(default=False)
    is_single = fields.Boolean(default = False)

    
    spouse_id = fields.Many2one(comodel_name="res.partner", string="Name", required=False, )
    reference_id = fields.Many2one(comodel_name="res.partner", string="Name", )
    reference_ids = fields.One2many(comodel_name="res.partner", inverse_name="reference_id", string="Name", required=False,  )
    # user_evaluate = fields.Many2one(comodel_name="res.users",
    #                                 string="Evaluated by",
    #                                 readonly=1,
    #                                 )
    # user_approve = fields.Many2one(comodel_name="res.users",
    #                                 string="Approved by",
    #                                 readonly=1,
    #                                 )
    # user_note = fields.Many2one(comodel_name="res.users",
    #                                 string="Noted by",
    #                                 readonly=1,
    #                                 )

    _sql_constraints = [('todo_task_name_uniq','UNIQUE (name,active)','Customer Already Exist')]


    # state = fields.Selection([
    #     ('draft', "Draft"),
    #     ('eval', "Evaluated"),
    #     ('apro', "Approved"),
    #     ('note','Noted'),
    # ], default='draft')

    state_1 = fields.Selection([
        ('step1', 'General Information'),
        ('step2', 'Billing Address'),])

    mothermaiden = fields.Many2one(comodel_name="res.partner",
                                   string="Mother's Maiden Name",
                                   required=False,
                                   domain=[('active', '=', True),('customer','=',True)]
                                   )

    policies_ids = fields.Many2many(comodel_name="interment.policy", required=False )
    policy_name = fields.Text()
    


    # @api.model
    # def spouse_select(self):
    #

    # @api.model
    # def _get_default_country(self):
    #     print"yes", 95
    #     return 95


   
    @api.onchange('employment_state')
    def onchange_employment_state(self):
        self.is_others = (self.employment_state == 'others')
        
    @api.onchange('employment_state_1')
    def onchange_employment_state_1(self):
        self.is_unemployed = (self.employment_state_1 == 'unemployed')

    @api.onchange('marital')
    def onchange_marital(self):
        self.is_single = (self.marital == 'single') or (self.marital == 'singleparent')
        
    @api.onchange('street')
    def onchange_street(self):
        self.street = self.street.title().strip() if self.street else False

    @api.onchange('name','first_name', 'middle_name', 'last_name', 'suffix',)
    def onchange_name(self):

        if self.is_company == False:
            x_name = ''
            sep = ', '
            suffix_ids = self.suffix
            if self.last_name:
                lname = self.last_name.title().strip()
            else:
                lname = ''
        
            if lname:
                x_name = '%s%s' % (lname, sep)
        
            if self.first_name:
                fname = self.first_name.title().strip()
            else:
                fname = ''
        
            if fname:
                x_name = '%s%s%s' % (x_name, ' ', fname)
        
            if self.suffix:
                suffix = self._get_suffix(suffix_ids)
            else:
                suffix = ''
        
            if suffix:
                x_name = '%s%s%s' % (x_name, ' ', suffix)
        
            if self.middle_name:
                mname = self.middle_name.title().strip()
            else:
                mname = ''
        
            if mname:
                x_name = '%s%s%s' % (x_name, ' ', mname)
        
            # if self.mothermaiden:
            #     mm = self.mothermaiden.title().strip()
            # else:
            #     mm = ''
            # if mm:
            #     self.mothermaiden = '%s' % mm
        
            self.name = x_name
        
            self.first_name = fname.title().strip()
            self.middle_name = mname.title().strip()
            self.last_name = lname.title().strip()
            # self.suffix = suffix.title().strip()
        else:
            if self.name:
                g_name = self.name
            else:
                g_name = ''

            if g_name:
                x_name = '%s' % g_name

            self.name = x_name.title().strip()

        

    @api.multi
    def _get_suffix(self, values):
        if values == 'jr':
            suffix = 'Jr'
        elif values == 'sr':
            suffix = 'Sr'

        elif values == 'ii':
            suffix = 'II'

        elif values == 'iii':
            suffix = 'III'

        elif values == 'iv':
            suffix = 'IV'

        elif values == 'v':
            suffix = 'V'

        elif values == 'vi':
            suffix = 'VI'

        elif values == 'vii':
            suffix = 'VII'

        else:
            suffix = ''

        return suffix

    @api.model
    def create(self, values):

        if values['is_company'] == False:
            fname = values['first_name']
            mname = values['middle_name']
            lname = values['last_name']
            suffix_ids = values['suffix']
            suffix = self._get_suffix(suffix_ids)
            values['name'] = "%s, %s %s %s" % (lname, fname, suffix, mname)
            values['first_name'] = fname
            values['middle_name'] = mname
            values['last_name'] = lname
            values['suffix'] = suffix_ids
        else:
            g_name = values['name']
            values['name'] = "%s" % (g_name)

        # if values.get('ClientNo',_('New')) == _('New'):
        #     values['ClientNo'] = self.env['ir.sequence'].next_by_code('res.partner') or _('New')

        rec = super(client, self).create(values)

        return rec

    @api.multi
    def write(self, values):

        rec = None
       
        if 'parent_id' not in values:
            if self.is_company == False:
                if 'first_name' in values and values['first_name']:
                    fname = values['first_name'].title().strip()
                elif 'first_name' not in values and self.first_name:
                    fname = self.first_name.title().strip()
                else:
                    fname = ''
        
                if 'middle_name' in values and values['middle_name']:
                    mname = values['middle_name'].title().strip()
                elif 'middle_name' not in values and self.middle_name:
                    mname = self.middle_name.title().strip()
                else:
                    mname = ''
        
                if 'last_name' in values and values['last_name']:
                    lname = values['last_name'].title().strip()
                elif 'last_name' not in values and self.last_name:
                    lname = self.last_name.title().strip()
                else:
                    lname = ''
        
                if 'suffix' in values and values['suffix']:
                    suffix = values['suffix']
                elif 'suffix' not in values and self.suffix:
                    suffix = self.suffix
                else:
                    suffix = ' '
        
                if suffix:
                    suffix = self._get_suffix(suffix)
        
                if 'first_name' in values and values['first_name'] or 'middle_name' in values and values[
                    'middle_name'] or 'last_name' in values and values['last_name']:
                    values['name'] = "%s, %s %s %s" % (lname, fname, suffix, mname)
                else:
                    values['name'] = self.name
    
                values['first_name'] = fname
                values['middle_name'] = mname
                values['last_name'] = lname
            else:
                values['name'] = self.name
        rec = super(client, self).write(values)
        return rec

    @api.model
    def _get_age(self):
        """Updates age field when birth_date is changed"""
        for s in self:
            if s.birthdate:
                d1 = datetime.strptime(s.birthdate, "%Y-%m-%d").date()
                d2 = date.today()
                s.age = relativedelta(d2, d1).years

    @api.model
    def update_age(self):
        """Updates age field for all partners once a day"""
        for rec in self.env['res.partner'].search([]):
            if rec.birthdate:
                d1 = datetime.strptime(rec.birthdate, "%Y-%m-%d").date()
                d2 = date.today()
                rec.age = relativedelta(d2, d1).years

    
    
    
class ClientReligion(models.Model):
    _name = 'client.religion'

    name = fields.Char(string="Religion")
    active = fields.Boolean(string="Active",default=True)
