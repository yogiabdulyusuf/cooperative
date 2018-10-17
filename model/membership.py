from odoo import api, fields, models
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, Warning
import logging

_logger = logging.getLogger(__name__)

STATES = [('draft', 'Draft'), ('in_progress', 'In Progress'), ('active', 'Active'), ('done', 'Done')]

class Membership(models.Model):
    _inherit = 'res.partner'

    @api.one
    def generate_account(self):
        #Generate Saving Account For Member
        savings_account_obj = self.env['savings.account']
        vals = {}
        vals.update({'interest': 'flat'})
        vals.update({'name': self.id})
        savings_account = savings_account_obj.create(vals)
        if savings_account:
            #Generate Transaksi Simpanan Pokok
            savings_trans_obj = self.env['savings.trans']
            vals = {}
            vals.update({'account_number_id': savings_account.id})
            principal_savings = self.env.user.company_id.principal_savings_trans_type_id
            if not principal_savings:
                raise ValidationError("Pricinpal Savings not defined,  please define on company information!")
            vals.update({'debit': self.env.user.company_id.principal_savings})
            vals.update({'saving_method' : 'deposit'})
            vals.update({'credit': 0.0})
            vals.update({'trans_type_id':principal_savings.id})
            saving_trans = savings_trans_obj.create(vals)
            if not saving_trans:
                raise ValidationError("Error Creating Simpanan Pokok")

            # Generate Transaksi Simpanan Wajib
            mandatory_savings = self.env.user.company_id.mandatory_savings_trans_type_id
            if not mandatory_savings:
                raise ValidationError("Mandatory Savings not defined, please define on company information!")
            vals = {}
            vals.update({'account_number_id': savings_account.id})
            vals.update({'debit': self.env.user.company_id.mandatory_savings})
            vals.update({'saving_method': 'deposit'})
            vals.update({'credit': 0.0})
            vals.update({'trans_type_id': mandatory_savings.id})
            saving_trans = savings_trans_obj.create(vals)
            if not saving_trans:
                raise ValidationError("Error Creating Simpanan Wajib")
        else:
            raise ValidationError("Error Creating Saving Account")


    @api.model
    def create(self, vals):
        res = super(Membership, self).create(vals)
        res.generate_account()
        return res

    active_members       = fields.Boolean(string="Active Member", )
    savings_account_id   = fields.One2many(comodel_name="savings.account", inverse_name="name",  )
    states               = fields.Selection(string="State", selection=STATES, required=True, default='draft', )

class Termination(models.Model):
    _name = 'member.termination'
    _rec_name = 'termination_id'
    _description = 'Member Termination'

    @api.one
    def trans_open(self):
        self.state = "open"

    @api.model
    def create(self, vals):
        vals['termination_id'] = self.env['ir.sequence'].next_by_code('member.termination')
        res = super(Termination, self).create(vals)
        res.trans_open()
        return res

    termination_id = fields.Char(string="Termination ID", readonly="True")
    date = fields.Datetime(string="Date", required=True, readonly="True", default=fields.Datetime.now)
    member_id = fields.Many2one(comodel_name="res.partner", string="Member ID", required=True, )
    state = fields.Selection(string="State", selection=[('draft', 'Draft'), ('open', 'Open'), ('review', 'Review'), ('request', 'Request'), ('approve', 'Approve'), ('done', 'Done'), ], required=False, default="draft")



