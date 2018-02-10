from odoo import api, fields, models 

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.onchange('name', 'first_name', 'middle_name', 'last_name', 'suffix', )
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