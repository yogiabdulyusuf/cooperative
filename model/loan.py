from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

STATES = [('draft', 'Draft'), ('request', 'Request'), ('review', 'Review'), ('approve', 'Approve'), ('reject', 'Reject'), ('done', 'Done'), ]


# LOAN TYPE
class LoanType(models.Model):
    _name = 'loan.type'
    _rec_name = 'loan_type'
    _description = 'Loan Type'

    loan_type   = fields.Char(string="Loan Type", required=True, )
    value       = fields.Integer(string="Max", required=True, )
    choice      = fields.Selection(string="Choice", selection=[('month', 'Month'), ('year', 'Year'), ], required=True, )


# LOAN INTEREST
class LoanInterest(models.Model):
    _name = 'loan.interest'
    _description = 'Loan Interest'

    name = fields.Char(string="Name", required=True, )
    interest    = fields.Float(string="Interest",  required=True, )


# LOAN TRANSACTION
class LoanTrans(models.Model):
    _name = 'loan.trans'
    _rec_name = 'trans_number'
    _description = 'Loan Transaction'


    trans_number        = fields.Integer(string="Transaction Number", required=False, )
    loan_type           = fields.Many2one(comodel_name="loan.type", string="Loan Type", required=True, )
    name                = fields.Many2one(comodel_name="loan.interest", string="Interest Type", required=True, )
    date_loan_trans     = fields.Date(string="Date", required=True, )
    estimate_start_date = fields.Date(string="Estimate Start Date", required=True, )
    installment         = fields.Char(string="Installment", required=True, )
    amount              = fields.Float(string="Amount",  required=True, )
    state               = fields.Selection(string="", selection=STATES, required=True, default='draft' )


# LOAN TRANSACTION LINE
class LoanTransLine(models.Model):
    _name = 'loan.trans_line'
    _description = 'Loan Transaction Line'

    sequence            = fields.Char(string="Sequence", required=False, )
    due_date            = fields.Date(string="Due Date", required=True, )
    amount_trans_line   = fields.Float(string="Amount",  required=True, )
    state = fields.Selection(string="", selection=[('open', 'Open'), ('done', 'Done'), ], required=True, default="open" )