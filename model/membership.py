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
            vals.update({'account_number': savings_account.id})
            principal_savings = self.env.user.company_id.principal_savings_trans_type_id
            if not principal_savings:
                raise ValidationError("Pricinpal Savings not defined,  please define on company information!")
            vals.update({'debit': self.env.user.company_id.principal_savings})
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
            vals.update({'account_number': savings_account.id})
            vals.update({'debit': self.env.user.company_id.mandatory_savings})
            vals.update({'credit': 0.0})
            vals.update({'trans_type_id': mandatory_savings.id})
            saving_trans = savings_trans_obj.create(vals)
            if not saving_trans:
                raise ValidationError("Error Creating Simpanan Wajib")
        else:
            raise ValidationError("Error Creating Saving Account")

        #for s in range(2):
        #    if s == 0:
        #        savings_account_obj = self.env['savings.account']
        #        vals = {}
        #        #vals.update({'account_number': account_number_obj})
        #        vals.update({'interest': 'flat'})
        #        vals.update({'name': self.id})
        #        savings_account_obj.create(vals)
        #    else:
        #        # GENERATE TRANS
        #        savings_trans_obj = self.env['savings.trans']
        #       # val_account = self.env['savings.account'].search({('account_number', '=', account_number_obj)})
        #        credit_val = 0
        #
        #        for i in range(2):
        #            if i == 0:
        #                debit_val = 300000
        #            else:
        #                debit_val = 50000
        #
        #            vals = {}
        #            #vals.update({'account_number': self.val_account.id})
        #            vals.update({'debit': debit_val})
        #            vals.update({'credit': credit_val})
        #            savings_trans_obj.create(vals)

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

    termination_id = fields.Char(string="Termination ID", required=True, )
    member_id = fields.Many2one(comodel_name="res.partner", string="Member ID", required=True, )
    descrip = fields.Text(string="Description", required=False, )



