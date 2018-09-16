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
    date = fields.Datetime(string="Date Today", required=False, )
    amount = fields.Float(string="Amount SHU",  required=False, )
    loan_services_percen = fields.Float(string="Loan Services %", required=False, )
    purchase_service_percen = fields.Float(string="Purchase Service %", required=False, )
    deposit_services_percen = fields.Float(string="Deposit Services %", required=False, )
    loan_services    = fields.Float(string=":", compute='calculate_loan_services', required=False, )
    purchase_service = fields.Float(string=":", compute='calculate_purchase_service', required=False, )
    deposit_services = fields.Float(string=":", compute='calculate_deposit_services', required=False, )

class journalSHU(models.Model):
    _name = 'journal.shu'
    _description = 'Journal SHU'

    date = fields.Datetime(string="Date today", required=False, )
    shuallocated_id = fields.Many2one(comodel_name="shu.allocated", string="SHU", required=False, )


