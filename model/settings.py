from odoo import api, fields, models


class Settings(models.Model):
    _inherit = 'res.company'

    principal_savings = fields.Float(string="Principal Savings", required=False, )
    mandatory_savings = fields.Float(string="Mandatory Savings", required=False, )
    principal_savings_trans_type_id = fields.Many2one('transaction.type', 'PS Transaction Type')
    mandatory_savings_trans_type_id = fields.Many2one('transaction.type', 'MS Transaction Type')
    account_company_id = fields.Many2one('account.account', 'Account Company')
    account_cash_id = fields.Many2one('account.account', 'Account Cash')
    jurnal_endofday_id = fields.Many2one('account.journal', 'Journal End Of Day')

