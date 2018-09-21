from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, Warning
from datetime import datetime, timedelta
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


    @api.one
    def calculate_percen(self):
        if self.loan_services_percen != 0.0:
            total_loan_services = self.amount * self.loan_services_percen / 100
            self.loan_services = total_loan_services

        if self.purchase_service_percen != 0.0:
            total_purchase_service = self.amount * self.purchase_service_percen / 100
            self.purchase_service = total_purchase_service

        if self.savings_services_percen != 0.0:
            total_savings_services = self.amount * self.savings_services_percen / 100
            self.savings_services = total_savings_services


        args = [('date_year', '=', self.year_shu)]
        res = self.env['savings.trans'].search(args)
        total_debit = 0
        total_credit = 0
        for data_detail in res:
            total_debit = total_debit + data_detail.debit
            total_credit = total_credit + data_detail.credit
        self.debit = total_debit
        self.credit = total_credit
        self.debit_and_credit = total_debit + total_credit

    @api.model
    def create(self, vals):
        res = super(shuAllocated, self).create(vals)
        res.calculate_percen()
        return res

    year_shu = fields.Integer(string="SHU", required=False, )
    date = fields.Datetime(string="Date", required=False, )
    amount = fields.Float(string="Amount",  required=False, )
    loan_services_percen = fields.Float(string="Loan Services %", required=False, default=0.0)
    purchase_service_percen = fields.Float(string="Purchase Service %", required=False, default=0.0)
    savings_services_percen = fields.Float(string="Savings Services %", required=False, default=0.0)
    loan_services    = fields.Float(string="Loan Services", required=False, default=0.0)
    purchase_service = fields.Float(string="Purchase Service", required=False, default=0.0)
    savings_services = fields.Float(string="Savings Services", required=False, default=0.0)
    debit = fields.Float(string="Calculate Debit 1 Year", default=0.0)
    credit = fields.Float(string="Calculate Credit 1 Year", default=0.0)
    debit_and_credit = fields.Float(string="Calculate Debit + Credit 1 Year", default=0.0)


class journalSHU(models.Model):
    _name = 'journal.shu'
    _description = 'Journal SHU'

    @api.one
    def generate_trans_shu(self):
        args = [('', '=', self.year_shu)]
        res = self.env['savings.trans'].search(args)

    @api.model
    def process_shu(self , vals):
        res = super(journalSHU, self).create(vals)  # Super berfungsi memanggil model ketika eksekusi create
        res.generate_trans_shu()                 # Menjalankan generate_saving_trans()
        return res

    date = fields.Datetime(string="Date today", required=False, )
    shuallocated_id = fields.Many2one(comodel_name="shu.allocated", string="SHU", required=False, )
    savings_trans_id = fields.One2many(comodel_name="savings.trans", inverse_name="journal_shu_id",
                                      string="Transactions")
    state = fields.Selection(string="state", selection=[('open', 'Open'), ('done', 'Done'), ], required=False, default='open')

