from odoo import api, fields, models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, Warning
import logging

_logger = logging.getLogger(__name__)

STATES = [('draft', 'Draft'),
          ('request', 'Request'),
          ('review', 'Review'),
          ('approve', 'Approve'),
          ('reject', 'Reject'),
          ('done', 'Done'),
          ]

# LOAN TYPE
class LoanType(models.Model):
    _name = 'loan.type'
    _description = 'Loan Type'

    name  = fields.Char(string="Name", required=True, )
    maximum_amount = fields.Integer(string="Maximum Amount", required=True, )
    payment_option = fields.Selection(string="Payment Option", selection=[('month', 'Monthly'), ('year', 'Yearly'), ], required=True, )
    interest_type = fields.Selection([('flat','Flat'), ('efektif','Efektif'), ('anuitas','Anuitas'),], 'Interest Type', default='flat', required=True)
    interest_percentage = fields.Float('Interest Percentage', default=0.0, required=True)
    iface_agunan = fields.Boolean('Agunan', default=False)
    agunan_amount = fields.Float(string="Agunan Min Amount", default=0.0)

# LOAN TRANSACTION
class LoanTrans(models.Model):
    _name = 'loan.trans'
    _rec_name = 'trans_number'
    _description = 'Loan Transaction'


    @api.one
    def trans_request(self):
        self.state = 'request'

    @api.one
    def trans_review(self):
        self.state = 'review'


    @api.one
    def trans_generate_line(self):
        loan_trans_line_obj = self.env['loan.trans.line']

        if self.loan_type_id.interest_type == "flat":

            installment_amount = self.amount / self.installment_number
            interest_amount = self.amount * self.loan_type_id.interest_percentage / 100 / self.installment_number
            installment_total = installment_amount + interest_amount
            for i in range(self.installment_number):
                vals = {}
                vals.update({'loan_trans_id': self.id})
                vals.update({'sequence': i + 1})
                vals.update({'name': 'Installment ke ' + str(i + 1)})
                vals.update(
                    {'due_date': datetime.strptime(self.estimate_start_date, '%Y-%m-%d') + relativedelta(months=i + 1)})
                vals.update({'installment_amount': installment_amount})
                vals.update({'interest_amount': interest_amount})
                vals.update({'installment_total': installment_total})
                loan_trans_line_obj.create(vals)

        elif self.loan_type_id.interest_type == "efektif":

            for i in range(self.installment_number):

                installment_amount = self.amount / self.installment_number
                interest_amount = (self.amount - ((i + 1 - 1) * installment_amount) * self.loan_type_id.interest_percentage / 100) / self.installment_number
                installment_total = installment_amount + interest_amount

                vals = {}
                vals.update({'loan_trans_id': self.id})
                vals.update({'sequence': i + 1})
                vals.update({'name': 'Installment ke ' + str(i + 1)})
                vals.update(
                    {'due_date': datetime.strptime(self.estimate_start_date, '%Y-%m-%d') + relativedelta(months=i + 1)})
                vals.update({'installment_amount': installment_amount})
                vals.update({'interest_amount': interest_amount})
                vals.update({'installment_total': installment_total})
                loan_trans_line_obj.create(vals)

        elif self.loan_type_id.interest_type == "anuitas":

            sisa_pinjaman_pokok = self.amount

            for i in range(self.installment_number):
                interest_amount = sisa_pinjaman_pokok * self.loan_type_id.interest_percentage / 100 / 12
                installment_total = (self.amount * (self.loan_type_id.interest_percentage / 100 /12)) / ( 1-1 / (1 + self.loan_type_id.interest_percentage / 100 / 12) ** self.installment_number)
                installment_amount = installment_total - interest_amount

                sisa_pinjaman_pokok = sisa_pinjaman_pokok - installment_amount

                vals = {}
                vals.update({'loan_trans_id': self.id})
                vals.update({'sequence': i + 1})
                vals.update({'name': 'Installment ke ' + str(i + 1)})
                vals.update(
                    {'due_date': datetime.strptime(self.estimate_start_date, '%Y-%m-%d') + relativedelta(months=i + 1)})
                vals.update({'installment_amount': installment_amount})
                vals.update({'interest_amount': interest_amount})
                vals.update({'installment_total': installment_total})
                loan_trans_line_obj.create(vals)
        else:
            raise ValidationError("Interest Type not defined,  please define on Interest Type !")
        # elif self.loan_type_id.interest_type is "tetap":
        #     funcTetap()

    trans_number = fields.Char(string="Transaction Number", readonly=True)
    member_id = fields.Many2one('res.partner','Member', domain=[('active_members','=', True)],required=True)
    date = fields.Datetime(string="Date", required=True, readonly="True", default=fields.Datetime.now)
    loan_type_id = fields.Many2one(comodel_name="loan.type", string="Loan Type", required=True, )
    estimate_start_date = fields.Date(string="Estimate Start Date", required=True, )
    installment_number = fields.Integer('Installment #', default=3, required=True)
    amount = fields.Float(string="Amount",  required=True, )
    state = fields.Selection(string="Status", selection=STATES, required=True, default='draft' )
    loan_trans_line = fields.One2many(comodel_name="loan.trans.line", inverse_name="loan_trans_id", string="Loan Trans Line", )

    @api.model
    def create(self, vals):
        vals['trans_number'] = self.env['ir.sequence'].next_by_code('loan.trans')
        res = super(LoanTrans, self).create(vals)
        res.trans_generate_line()
        return res


# LOAN TRANSACTION LINE
class LoanTransLine(models.Model):
    _name = 'loan.trans.line'
    _description = 'Loan Transaction Line'

    @api.one
    def get_state(self):
        for line in self:
            if line.loan_trans_id.state == 'draft':
                line.state = 'draft'
            if line.loan_trans_id.state == 'request':
                line.state = 'request'
            if line.loan_trans_id.state == 'review':
                line.state = 'review'
            if line.loan_trans_id.state == 'approve':
                line.state = 'approve'
            if line.loan_trans_id.state == 'reject':
                line.state = 'reject'
            if line.loan_trans_id.state == 'done':
                line.state = 'done'

    loan_trans_id  = fields.Many2one("loan.trans", "Loan Trans Line Header", ondelete="cascade")
    sequence = fields.Integer('Sequence', readonly=True)
    name = fields.Char(string="Name", required=True, )
    due_date = fields.Date(string="Due Date", required=True, )
    installment_amount = fields.Float(string="Installment Amount",  required=True, default=0.0)
    interest_amount = fields.Float('Interest Amount', required=True, default=0.0)
    installment_total = fields.Float('Total Amount', required=True, default=0.0)
    iface_request_review = fields.Boolean('Review', default=False, readonly=True)
    date_request_review = fields.Datetime('Review Date', readony=True)
    iface_request_approval = fields.Boolean('Approval', default=False, readonly=True)
    date_request_approval = fields.Datetime('Approval Date', readony=True)
    billing_id = fields.Many2one(comodel_name="billing.periode.line", string="Billing ID", )
    loan_invoice_ids = fields.One2many('account.invoice','loan_trans_line_id', 'Invoices', readonly=True)
    billing_id = fields.Many2one(comodel_name="billing.periode.line", string="Billing Id", required=False, )
    state = fields.Selection(STATES, "Status", compute='get_state', required=True)

