from odoo import api, fields, models


class Settings(models.Model):
    _inherit = 'res.company'

    principal_savings = fields.Float(string="Principal Savings", required=False, )
    mandatory_savings = fields.Float(string="Mandatory Savings", required=False, )
