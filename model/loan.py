from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

STATES = [('draft', 'Draft'),
          ('request', 'Request'),
          ('review', 'Review'),
          ('approve', 'Approve'),
          ('reject', 'Reject'),
          ('done', 'Done'),
          ]

# LOAN TYPE
class LoanType(models.Model):
    _name = 'loan.type'
    _rec_name = 'loan_type'
    _description = 'Loan Type'

    loan_type   = fields.Char(string="Loan Type", required=True, )
    value       = fields.Integer(string="Max", required=True, )
    choice      = fields.Selection(string="Choice", selection=[('month', 'Month'), ('year', 'Year'), ], required=True, )
    agunan      = fields.Text(string="Agunan", required=False, )
    advance_money = fields.Float(string="Advance",  required=False, )


# LOAN TRANSACTION
class LoanTrans(models.Model):
    _name = 'loan.trans'
    _rec_name = 'trans_number'
    _description = 'Loan Transaction'

    trans_number = fields.Char(string="Transaction Number", )
    loan_type = fields.Many2one(comodel_name="loan.type", string="Loan Type", required=True, )
    loan_interest = fields.Selection(string="Loan Interest", selection=[('flat', 'Flat'), ('fluktuatif', 'Fluktuatif'), ], required=True, )
    date_loan_trans = fields.Datetime(string="Date", required=True, readonly="True", default=fields.Datetime.now)
    estimate_start_date = fields.Date(string="Estimate Start Date", required=True, )
    quantity = fields.Float(string="Quantity",  required=True, )
    state = fields.Selection(string="", selection=STATES, required=True, default='draft' )
    loan_trans_line = fields.One2many(comodel_name="loan.trans_line", inverse_name="loan_trans_line_id", string="Loan Trans Line", )

    @api.model
    def create(self, vals):
        vals['trans_number'] = self.env['ir.sequence'].next_by_code('loan.trans')
        return super(LoanTrans, self).create(vals)


# LOAN TRANSACTION LINE
class LoanTransLine(models.Model):
    _name = 'loan.trans.line'
    _description = 'Loan Transaction Line'

    @api.one
    def get_state(self):
        for line in self:
            line.state = 'open'

    loan_trans_line_id  = fields.Many2one(comodel_name="loan.trans", string="Loan Trans Line Header", required=True, )
    sequence = fields.Integer('Sequence', readonly=True)
    installment = fields.Char(string="Installment", required=True, )
    billing_periode_line_id = fields.Many2one('billing.periode.line', 'Periode Line #', readonly=True)
    due_date = fields.Date(string="Due Date", required=True, )
    amount = fields.Float(string="Amount",  required=True, )
    state = fields.Selection(string="", selection=[('open', 'Open'), ('done', 'Done'), ], compute='get_state', required=True)
    loan_invoice_ids = fields.One2many('account.invoice','loan_trans_line_id', 'Invoices', readonly=True)

