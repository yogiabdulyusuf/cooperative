from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

STATES = [('open', 'Open'), ('done', 'Done')]


# SAVINGS TYPE
class Savings(models.Model):
    _name = 'savings.type'
    _rec_name = 'name_savings_type'

    name_savings_type = fields.Char(string="Savings Type", required=True, )

# SAVINGS TYPE INTEREST
class SavingAccountType(models.Model):
    _name = 'savings.account.type'
    _description = 'Interest'

    name = fields.Char(string="Name", required=True, )
    interest = fields.Float(string="Interest",  required=True, )


# SAVINGS TRANSACTION

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


    trans_number        = fields.Integer(string="Transaction Number", required=True, )
    date                = fields.Date(string="Date", required=True, )
    account_number      = fields.Many2one(comodel_name="savings.account", string="Savings Account", required=True, )
    amount              = fields.Float(string="Amount",  required=True, )
    state               = fields.Selection(string="", selection=STATES, required=True, default='open' )

# SAVINGS ACCOUNT
class SavingsAccount(models.Model):
    _name = 'savings.account'
    _rec_name = 'account_number'
    _description = 'Savings Account'

    account_number = fields.Char(string="Account Number", required=True, )
    name = fields.Many2one(comodel_name="res.partner", string="Name", required=True, )