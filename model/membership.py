from odoo import api, fields, models

class Membership(models.Model):
    _inherit = 'res.partner'

    active_member       = fields.Boolean(string="Active Member", )
