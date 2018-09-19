from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class shuAllocated(models.Model):
    _name = 'shu.allocated'
    _rec_name = 'year_shu'
    _description = 'SHU Allocated'

    # @api.one
    # def calculate_loan_services(self):
    #
    #         total = total + (data_detail.debit - data_detail.credit) * self.loan_services_percen / 100
    #     self.balance = total


    year_shu = fields.Integer(string="Year SHU", required=False, )
    date = fields.Datetime(string="Date today", required=False, )
    amount = fields.Float(string="Amount SHU",  required=False, )
    loan_services_percen = fields.Float(string="Loan Services %", required=False, )
    purchase_service_percen = fields.Float(string="Purchase Service %", required=False, )
    savings_services_percen = fields.Float(string="Savings Services %", required=False, )
    loan_services    = fields.Float(string="Loan Services", compute='calculate_loan_services', required=False, )
    purchase_service = fields.Float(string="Purchase Service", compute='calculate_purchase_service', required=False, )
    savings_services = fields.Float(string="Savings Services", compute='calculate_deposit_services', required=False, )
    debit = fields.Float(string="Calculate Debit 1 Year", default=0.0)
    credit = fields.Float(string="Calculate Credit 1 Year", default=0.0)
    debit_and_credit = fields.Float(string="Calculate Debit + Credit 1 Year", default=0.0)


class journalSHU(models.Model):
    _name = 'journal.shu'
    _description = 'Journal SHU'

    date = fields.Datetime(string="Date today", required=False, )
    shuallocated_id = fields.Many2one(comodel_name="shu.allocated", string="SHU", required=False, )
    savings_list_id = fields.One2many(comodel_name="savings.trans", inverse_name="account_number_id",
                                      string="Transactions")
    state = fields.Selection(string="state", selection=[('open', 'Open'), ('done', 'Done'), ], required=False, default='open')

