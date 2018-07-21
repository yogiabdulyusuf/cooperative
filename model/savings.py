from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

STATES = [('open', 'Open'), ('done', 'Done')]


# SAVINGS TYPE
class Savings(models.Model):
    _name = 'savings.type'
    _rec_name = 'name_savings_type'

    name_savings_type = fields.Char(string="Savings Type", required=True, )


# SAVINGS TRANSACTION

class SavingsTransaction(models.Model):
    _name = 'savings.trans'
    _rec_name = 'saving_trans_id'
    _description = 'Savings Transaction'


    @api.one
    def trans_close(self):
        self.state="done"

    @api.one
    def trans_re_open(self):
        self.state = "open" #pindah state ke open


    saving_trans_id = fields.Char(string="Transaction Number", required=True, )
    date            = fields.Date(string="Date", required=True, )
    trans_type      = fields.Selection(string="Transaction Type", selection=[('deposits', 'Deposits'), ('taking', 'Taking'), ], required=True, )
    account_number  = fields.Many2one(comodel_name="savings.account", string="Savings Account", required=True, )
    amount          = fields.Float(string="Amount", required=True, )
    state           = fields.Selection(string="", selection=STATES, required=True, default='open' )

# SAVINGS ACCOUNT
class SavingsAccount(models.Model):
    _name = 'savings.account'
    _rec_name = 'account_number'
    _description = 'Savings Account'

    account_number     = fields.Char(string="Account Number", required=True, )
    interest           = fields.Selection(string="Savings Interest", selection=[('flat', 'Flat'), ('fluktuatif', 'Fluktuatif'), ], required=True, )
    name               = fields.Many2one(comodel_name="res.partner", string="Name", required=True, )
    principal_savings  = fields.Float(string="Principal Savings",  required=False, )
    mandatory_savings  = fields.Float(string="Mandatory Savings", required=False, )
    amount             = fields.Float(string="Amount", required=True, )
    savings_list       = fields.One2many(comodel_name="savings.list", inverse_name="saving_list_id", string="Savings List", )

# SAVINGS list
class SavingsList(models.Model):
    _name = 'savings.list'
    _description = 'Savings List'

    saving_list_id = fields.Many2one(comodel_name="savings.account", string="saving list header", required=True, )
    date_savings = fields.Date(string="Date Savings", required=True, )
    voluntary_savings = fields.Float(string="Voluntary Savings", required=False, )
    mandatory_savings = fields.Float(string="Mandatory Savings",  required=False, )