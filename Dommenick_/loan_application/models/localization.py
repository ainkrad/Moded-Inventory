# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ConfigRegion(models.Model):
    _name = 'config.region'
    _description = 'Configure Region'
    _inherit = 'mail.thread'
    _mail_post_access = 'read'

    name = fields.Char(string='Name')
    region_code = fields.Char(string="Region Code")
    country_id = fields.Many2one('res.country',string='Country')
    active = fields.Boolean(string='Active',default="True")

    @api.model
    def create(self, values):
        if values['name']:
            values['name'] = values['name'].title()

        return super(ConfigRegion, self).create(values)

    @api.multi
    def write(self, values):
        if 'name' in values:
            if values['name']:
                values['name'] = values['name'].title()

        return super(ConfigRegion, self).write(values)

class ConfigProvince(models.Model):
    _name = 'config.province'
    _description = 'Configure Province'
    _inherit = 'mail.thread'
    _mail_post_access = 'read'

    name = fields.Char(string='Name')
    province_code = fields.Char(string="Province Code")
    region_id = fields.Many2one('config.region', string='Region')
    active = fields.Boolean(string='Active',default="True")

    @api.model
    def create(self, values):
        if values['name']:
            values['name'] = values['name'].title()

        return super(ConfigProvince, self).create(values)

    @api.multi
    def write(self, values):
        if 'name' in values:
            if values['name']:
                values['name'] = values['name'].title()

        return super(ConfigProvince, self).write(values)

class ConfigMunicipality(models.Model):
    _name = 'config.municipality'
    _description = 'Configure Municipality'
    _inherit = 'mail.thread'
    _mail_post_access = 'read'

    name = fields.Char(string='Name')
    municipality_code = fields.Char(string="Municipality/City Code")
    province_id = fields.Many2one('config.province', string='Province')
    active = fields.Boolean(string='Active',default="True")

    @api.model
    def create(self, values):
        if values['name']:
            values['name'] = values['name'].title()

        return super(ConfigMunicipality, self).create(values)

    @api.multi
    def write(self, values):
        if 'name' in values:
            if values['name']:
                values['name'] = values['name'].title()

        return super(ConfigMunicipality, self).write(values)

class ConfigBarangay(models.Model):
    _name = 'config.barangay'
    _description = 'Configure Barangay'
    _inherit = 'mail.thread'
    _mail_post_access = 'read'

    name = fields.Char(string='Name')
    barangay_code = fields.Char(string="Barangay Code")
    municipality_id = fields.Many2one('config.municipality', string='Municipality/City')
    active = fields.Boolean(string='Active',default="True")

    @api.model
    def create(self, values):
        if values['name']:
            values['name'] = values['name'].title()

        return super(ConfigBarangay, self).create(values)

    @api.multi
    def write(self, values):
        if 'name' in values:
            if values['name']:
                values['name'] = values['name'].title()

        return super(ConfigBarangay, self).write(values)

class ConfigZipcode(models.Model):
    _name = 'config.zipcode'
    _description = 'Configure Zip Code'
    _inherit = 'mail.thread'
    _mail_post_access = 'read'

    name = fields.Char(string="ZIP code")
    municipality_id = fields.Many2one('config.municipality', string="Municipality/City")

    @api.model
    def create(self, values):
        if values['name']:
            values['name'] = values['name'].title()

        return super(ConfigZipcode, self).create(values)

    @api.multi
    def write(self, values):
        if 'name' in values:
            if values['name']:
                values['name'] = values['name'].title()

        return super(ConfigZipcode, self).write(values)