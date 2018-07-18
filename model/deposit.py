from odoo import api, fields, models

# LONG DEPOSITS
class LongDeposit(models.Model):
    _name = 'long.deposits'
    _rec_name = 'long_deposits'
    _description = 'Long Deposits'

    long_deposits   = fields.Integer(string="Long Deposits", required=False, )
    choice_deposit  = fields.Selection(string="Choice", selection=[('month', 'Month'), ('year', 'Year'), ], required=True, )
