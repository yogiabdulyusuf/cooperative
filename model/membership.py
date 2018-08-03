from odoo import api, fields, models
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

STATES = [('draft', 'Draft'), ('in_progress', 'In Progress'), ('active', 'Active'), ('done', 'Done')]

class Membership(models.Model):
    _inherit = 'res.partner'

    @api.one
    def generate_account(self):
        savings_account_obj = self.env['savings.account']
        vals = {}
        vals.update({'interest': 'flat'})
        vals.update({'name' : self.id})
        savings_account_obj.create(vals)


    @api.one
    def generate_trans(self):
        savings_trans_obj = self.env['savings.trans']
        credit_val = 0
        date_now = fields.Datetime.now
        i = 0

        for i in range(2):
            if i == 0:
                debit_val = 300000
            else:
                debit_val = 50000

            vals = {}
            vals.update({'date': date_now})
            vals.update({'debit': 300000})
            vals.update({'credit': debit_val})
            vals.update({'trans_type_id': 'SPK'})
            i = i+1
            savings_trans_obj.create(vals)

    @api.model
    def create(self, vals):
        res = super(Membership, self).create(vals)
        res.generate_account()
        res.generate_trans()
        return res

    active_members       = fields.Boolean(string="Active Member", )
    savings_account_id   = fields.One2many(comodel_name="savings.account", inverse_name="name",  )
    states               = fields.Selection(string="State", selection=STATES, required=True, default='draft', )

class Termination(models.Model):
    _name = 'member.termination'
    _rec_name = 'termination_id'
    _description = 'Member Termination'

    termination_id = fields.Char(string="Termination ID", required=True, )
    member_id = fields.Many2one(comodel_name="res.partner", string="Member ID", required=True, )
    descrip = fields.Text(string="Description", required=False, )

