from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning


class AccountInvoice(models.Model):
    _inherit  = 'account.invoice'

    loan_trans_line_id  = fields.Many2one('loan.trans.line','Loan #', readonly=True)
