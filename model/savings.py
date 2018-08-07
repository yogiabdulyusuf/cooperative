from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

STATES = [('open', 'Open'), ('approve', 'Approve'), ('reject', 'Reject'), ('done', 'Done')]



# TRANSACTION TYPE
class TransactionType(models.Model):
    _name = 'transaction.type'
    _description = 'Transaction Type'

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.code + ' (' + record.name + ')'
            result.append((record.id,name))
        return result

    code = fields.Char(string="Code", size=3, required=True, )
    name = fields.Char(string="Name", required=True, )
    type = fields.Selection(string="Type", selection=[('debit', 'Debit'), ('credit', 'Credit'), ], required=True, )


# SAVINGS ACCOUNT
class SavingsAccount(models.Model):
    _name = 'savings.account'
    _rec_name = 'account_number'
    _description = 'Savings Account'

    @api.one
    def calculate_total_balance(self):
        total = 0
        for data_detail in self.savings_list:
            total = total + (data_detail.debit - data_detail.credit)
        self.balance = total

    account_number     = fields.Char(string="Account Number" )
    interest           = fields.Selection(string="Savings Interest", selection=[('flat', 'Flat'), ('fluktuatif', 'Fluktuatif'), ], required=True, default='flat')
    name               = fields.Many2one(comodel_name="res.partner", string="Name", domain=[('active_members','=', True)], required=True, )
    iface_default      = fields.Boolean('Default', default=False, readonly=True)
    balance            = fields.Float(string="Balance", compute='calculate_total_balance', readonly=True)
    savings_list       = fields.One2many(comodel_name="savings.trans", inverse_name="account_number", string="Transactions")

    @api.model
    def create(self, vals):
        vals['account_number'] = self.env['ir.sequence'].next_by_code('savings.account')
        return super(SavingsAccount, self).create(vals)

# SAVINGS TRANSACTION
class SavingsTransaction(models.Model):
    _name = 'savings.trans'
    _rec_name = 'saving_trans_id'
    _description = 'Savings Transaction'


    @api.one
    def trans_close(self):
        self.state="done"

    @api.one
    def trans_re_open(self):
        self.state = "open" #pindah state ke open

    @api.multi
    def trans_corection(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'CORECTION FORM FOR APPROVEL OR REJECT',
            'res_model': 'corection.deposit_withdrawal',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('corection_trans_view', False),
            'target': 'new',
        }

    @api.model
    def create(self, vals):
        vals['saving_trans_id'] = self.env['ir.sequence'].next_by_code('savings.trans')
        return super(SavingsTransaction, self).create(vals)

    @api.one
    def get_state(self):
        for line in self:
            line.state = 'open'

    saving_trans_id = fields.Char(string="Transaction Number", readonly=True )
    date            = fields.Datetime(string="Date", required=True, readonly=True, default=fields.Datetime.now)
    trans_type_id   = fields.Many2one(comodel_name="transaction.type", string="Transaction Type", )
    account_number  = fields.Many2one("savings.account", "Savings Account", )
    debit           = fields.Float(string="Debit",  default=0.0)
    credit          = fields.Float(string="Credit",  default=0.0)
    state           = fields.Selection(string="", selection=STATES, required=True, compute='get_state', default='open')

# koreksi setor & tarik
class Corection(models.Model):
    _name = 'corection.deposit_withdrawal'
    _rec_name = 'corection_id'
    _description = 'Koreksi Setor Tarik'

    corection_id = fields.Char(string="Corection ID", required=True, Readonly=True )
    savings_trans_id = fields.Many2one(comodel_name="savings.trans", string="Transaction ID", required=True, )
    description = fields.Text(string="Description", required=False, )
