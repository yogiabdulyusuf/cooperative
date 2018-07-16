from odoo import api, fields, models

class LoanType(models.Model):
    _name = 'loan.type'
    _rec_name = 'loan_type'
    _description = 'Loan Type'

    loan_type = fields.Char(string="Loan Type", required=True, )
    max       = fields.Integer(string="Max", required=True, )
    choice = fields.Selection(string="Choice", selection=[('month', 'Month'), ('year', 'Year'), ], required=True, )

# SAVINGS TYPE INTEREST
class LoanInterest(models.Model):
    _name = 'loan.interest'
    _rec_name = 'type_loan_interest'
    _description = 'Loan Interest'

    type_loan_interest = fields.Char(string="Type of Loan Interest", required=True, )
    value_loan_interest = fields.Float(string="Value of Loan Interest",  required=True, )