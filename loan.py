from odoo import api, fields, models

# LOAN TYPE
class LoanType(models.Model):
    _name = 'loan.type'
    _rec_name = 'loan_type'
    _description = 'Loan Type'

    loan_type = fields.Char(string="Loan Type", required=True, )
    max       = fields.Integer(string="Max", required=True, )
    choice = fields.Selection(string="Choice", selection=[('month', 'Month'), ('year', 'Year'), ], required=True, )


# LOAN INTEREST
class LoanInterest(models.Model):
    _name = 'loan.interest'
    _rec_name = 'type_loan_interest'
    _description = 'Loan Interest'

    type_loan_interest = fields.Char(string="Type of Loan Interest", required=True, )
    value_loan_interest = fields.Float(string="Value of Loan Interest",  required=True, )


# LOAN TRANSACTION
class LoanTrans(models.Model):
    _name = 'loan.trans'
    _rec_name = 'trans_number'
    _description = 'Loan Transaction'

    trans_number        = fields.Integer(string="Transaction Number", required=False, )
    date_loan_trans     = fields.Date(string="Date", required=True, )
    estimate_start_date = fields.Date(string="Estimate Start Date", required=True, )
    installment         = fields.Char(string="Installment", required=True, )
    amount              = fields.Float(string="Amount",  required=True, )