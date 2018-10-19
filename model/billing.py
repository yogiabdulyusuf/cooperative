from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning
from datetime import datetime, timedelta

class BillingPeriode(models.Model):
    _name = 'billing.periode'

    @api.one
    def trans_generate_line(self):
        billing_periode_line_obj = self.env['billing.periode.line']
        for i in range(12):
            i += 1
            firstday = datetime.strptime(str(self.name) + '-' + str(i).zfill(2) + '-' + '01', "%Y-%m-%d")
            if i < 12:
                lastday = datetime.strptime(str(self.name) + '-' + str(i+1).zfill(2) + '-' + '01', "%Y-%m-%d") + timedelta(days=-1)
            else:
                lastday = datetime.strptime(str(self.name + 1) + '-' + '01' + '-' + '01',"%Y-%m-%d") + timedelta(days=-1)
            vals  = {}
            vals.update({'billing_id': self.id})
            vals.update({'name': i})
            vals.update({'start_date': firstday})
            vals.update({'end_date': lastday})
            res = billing_periode_line_obj.create(vals)

    @api.one
    def generate_billing_savings(self):

        args = [('state', '=', 'active')]
        res = self.env['savings.account'].search(args)

        for data_detail in res:
            # Generate Transaksi Simpanan Wajib
            savings_trans_obj = self.env['savings.trans']

            mandatory_savings = self.env.user.company_id.mandatory_savings_trans_type_id
            if not mandatory_savings:
                raise ValidationError("Mandatory Savings not defined, please define on company information!")

            vals = {}
            vals.update({'account_number_id': data_detail.savings_account.id})
            vals.update({'debit': self.env.user.company_id.mandatory_savings})
            vals.update({'saving_method': 'deposit'})
            vals.update({'credit': 0.0})
            vals.update({'trans_type_id': mandatory_savings.id})
            vals.update({'state': 'openbilling'})
            saving_trans = savings_trans_obj.create(vals)

            if not saving_trans:
                raise ValidationError("Error Creating Simpanan Wajib")

    name = fields.Integer('Year', required=True)
    line_ids = fields.One2many('billing.periode.line','billing_id','Details', readonly=True)

    @api.model
    def create(self, vals):
        res = super(BillingPeriode, self).create(vals)
        res.trans_generate_line()
        # res.generate_billing_savings()
        return res

class BillingPeriodeLine(models.Model):
    _name = 'billing.periode.line'
    _rec_name = 'billing_id'

    name = fields.Integer('Month', required=True, readonly=True)
    billing_id = fields.Many2one('billing.periode','Periode #', readonly=True)
    start_date = fields.Date('Start Date', required=True, readonly=True)
    end_date = fields.Date('End Date', required=True, readonly=True)
    loan_trans_id = fields.One2many('loan.trans.line', 'billing_id', 'Loan Trans ID', readonly=True)
    loan_trans_line_id = fields.One2many(comodel_name="loan.trans.line", inverse_name="billing_id", string="Loan Trans", required=False, )
    state = fields.Selection([('open','Open'),('done','Close')], 'Status', default='open', readonly=True)
