from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, Warning
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class shuAllocated(models.Model):
    _name = 'shu.allocated'
    _rec_name = 'year_shu'
    _description = 'SHU Allocated'


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
    _rec_name = 'shu_number'
    _description = 'Journal SHU'

    @api.one
    def generate_trans_shu(self):
        args = [('state', '=', 'active')]
        res = self.env['savings.account'].search(args)

        for data_detail in res:
            val_savings = 0
            val_loan = 0
            # val_purchase = 0.0

            if self.shuallocated_id.savings_services_percen != 0:
                val_savings = data_detail.debit / self.shuallocated_id.debit * self.shuallocated_id.savings_services

            elif self.shuallocated_id.loan_services_percen != 0:
                val_loan = data_detail.credit / self.shuallocated_id.credit * self.shuallocated_id.loan_services

            # elif self.purchase_percen_val != 0.0:
            total_shu_didapat = val_savings + val_loan   # val_purchase

            # Generate Transaksi SHU
            savings_trans_obj = self.env['savings.trans']
            vals = {}
            vals.update({'account_number_id': data_detail.id})
            mandatory_savings = self.env.user.company_id.mandatory_savings_trans_type_id
            if not mandatory_savings:
                raise ValidationError("Pricinpal Savings not defined,  please define on company information!")
            vals.update({'debit': total_shu_didapat})
            vals.update({'saving_method': 'deposit'})
            vals.update({'credit': 0.0})
            vals.update({'trans_type_id': mandatory_savings.id})
            vals.update({'journal_shu_id': self.id})
            vals.update({'state': 'paid'})
            saving_trans = savings_trans_obj.create(vals)
            if not saving_trans:
                raise ValidationError("Error Creating Trans SHU")

        self.state = "done"

    # @api.model
    # def process_shu(self, vals):
    #     res = super(journalSHU, self).create(vals)  # Super berfungsi memanggil model ketika eksekusi create
    #     res.generate_trans_shu()                 # Menjalankan generate_saving_trans()
    #     return res

    @api.model
    def create(self, vals):
        vals['shu_number'] = self.env['ir.sequence'].next_by_code('journal.shu')
        res = super(journalSHU, self).create(vals)
        res.generate_trans_shu()
        return res

    shu_number = fields.Char(string="SHU Number")
    date = fields.Datetime(string="Date today", required=False, )
    shuallocated_id = fields.Many2one(comodel_name="shu.allocated", string="SHU", required=False, )
    savings_trans_id = fields.One2many(comodel_name="savings.trans", inverse_name="journal_shu_id",
                                      string="Transactions")
    state = fields.Selection(string="state", selection=[('new', 'New'), ('open', 'Open'), ('done', 'Done'), ], required=False, default='new')

