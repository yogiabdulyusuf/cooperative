from odoo import api, fields, models

class Savings(models.Model):
    _name = 'savings.type'
    _rec_name = 'name_savings_type'

    name_savings_type = fields.Char(string="Savings Type", required=True, )


class SavingInterest(models.Model):
    _name = 'savings.interest'
    _rec_name = 'type_interest'
    _description = 'Interest'

    type_interest = fields.Char(string="Type of Interest", required=True, )
    value_interest = fields.Float(string="Value of Interest",  required=True, )


class TransactionType(models.Model):
    _name = 'transaction.type'
    _rec_name = 'trans_type'
    _description = 'Transaction Type'

    trans_type = fields.Char(string="Transaction Type", required=True, )


class SavingsTransaction(models.Model):
    _name = 'savings.trans'
    _rec_name = 'trans_number'
    _description = 'Savings Transaction'

    trans_number = fields.Integer(string="Transaction Number", required=True, )
    date = fields.Date(string="Date", required=True, )
    amount = fields.Float(string="Amount",  required=True, )
    #state = fields.Selection([
    #   ('open', 'Open'),
    #   ('done', 'Done')
    #], 'Status', default='draft' )