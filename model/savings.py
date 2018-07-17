from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

# SAVINGS TYPE
class Savings(models.Model):
    _name = 'savings.type'
    _rec_name = 'name_savings_type'

    name_savings_type = fields.Char(string="Savings Type", required=True, )

# SAVINGS TYPE INTEREST
class SavingInterest(models.Model):
    _name = 'savings.interest'
    _rec_name = 'type_interest'
    _description = 'Interest'

    type_interest = fields.Char(string="Type of Savings Interest", required=True, )
    value_interest = fields.Float(string="Value of Savings Interest",  required=True, )

# TRANSACTION TYPE
class TransactionType(models.Model):
    _name = 'transaction.type'
    _rec_name = 'trans_type'
    _description = 'Transaction Type'

    trans_type = fields.Char(string="Transaction Type", required=True, )

# SAVINGS TRANSACTION

STATES = [('open','Open'), ('done','Done')]

class SavingsTransaction(models.Model):
    _name = 'savings.trans'
    _rec_name = 'trans_number'
    _description = 'Savings Transaction'


    @api.one
    def trans_close(self):
        self.state="done"

    @api.one
    def trans_re_open(self):
        self.state = "open" #pindah state ke open


    trans_number = fields.Integer(string="Transaction Number", required=True, )
    date = fields.Date(string="Date", required=True, )
    amount = fields.Float(string="Amount",  required=True, )
    state = fields.Selection(string="", selection=STATES, required=True, default='open' )

# SAVINGS ACCOUNT
class SavingsAccount(models.Model):
    _name = 'savings.account'
    _rec_name = 'account_number'
    _description = 'Savings Account'

    account_number = fields.Char(string="Account Number", required=True, )
    new_field_id = fields.Many2one(comodel_name="", string="Account Type", required=True, )
