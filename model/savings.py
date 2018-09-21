from odoo import api, fields, models
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, Warning
import logging

_logger = logging.getLogger(__name__)

STATES = [('new', 'New'), ('open', 'Open'), ('paid', 'Paid'), ('posted', 'Posted')]



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
        for data_detail in self.savings_list_id:
            total = total + (data_detail.debit - data_detail.credit)
        self.balance = total


    account_number     = fields.Char(string="Account Number" )
    interest           = fields.Selection(string="Savings Interest", selection=[('flat', 'Flat'), ('fluktuatif', 'Fluktuatif'), ], required=True, default='flat')
    name               = fields.Many2one(comodel_name="res.partner", string="Name", domain=[('active_members','=', True)], required=True, )
    iface_default      = fields.Boolean('Default', default=False, readonly=True)
    balance            = fields.Float(string="Balance", compute='calculate_total_balance', readonly=True)
    savings_list_id    = fields.One2many(comodel_name="savings.trans", inverse_name="account_number_id", string="Transactions")

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
    def trans_open(self):
        self.state = "open"  # pindah state ke open

    @api.one
    def trans_paid(self):
        self.state = "paid"

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


    saving_trans_id     = fields.Char(string="Transaction Number", readonly=True )
    date                = fields.Date(string="Date Paid", required=True, readonly=True, default=fields.Date.today())
    date_month          = fields.Integer(string="Date Month", required=False, default=datetime.now().strftime('%m'))
    date_year           = fields.Integer(string="Date Year", required=False, default=datetime.now().strftime('%Y'))
    trans_type_id       = fields.Many2one(comodel_name="transaction.type", string="Transaction Type", required=True )
    account_number_id   = fields.Many2one("savings.account", "Savings Account", required=True)
    journal_shu_id      = fields.Many2one("journal.shu", "Journal SHU", )
    endofday_id         = fields.Many2one("end.of.day", "End Of Day ID",)
    saving_method       = fields.Selection(string="Saving Method", selection=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal'), ], readonly=True )
    debit               = fields.Float(string="Debit",  default=0.0)
    credit              = fields.Float(string="Credit",  default=0.0)
    state               = fields.Selection(string="", selection=STATES, required=True, default='new')

# koreksi setor & tarik
class Corection(models.Model):
    _name = 'corection.deposit_withdrawal'
    _rec_name = 'corection_id'
    _description = 'Koreksi Setor Tarik'

    corection_id = fields.Char(string="Corection ID", required=True, Readonly=True )
    savings_trans_id = fields.Many2one(comodel_name="savings.trans", string="Transaction ID", required=True, )
    description = fields.Text(string="Description", required=False, )


class EndOfDay(models.Model):
    _name = 'end.of.day'
    _rec_name = 'endofday'
    _description = 'End OF Day'

    @api.one
    def calculate_total_balance(self):
        total = 0
        for data_detail in self.savings_list_id:
            total = total + (data_detail.debit - data_detail.credit)
        self.balance = total

    @api.one
    def generate_trans_post_jurnal(self):
        jurnal_entrie_obj = self.env['account.move']

        number = self.env['ir.sequence'].next_by_code('account.reconcile')

        label = 'EOD' + self.date_endofday

        jurnal_endofday = self.env.user.company_id.jurnal_endofday_id
        if not jurnal_endofday:
            raise ValidationError("Jurnal End Of Day not defined,  please define on company information!")

        account_company = self.env.user.company_id.account_company_id
        if not account_company:
            raise ValidationError("Account Company not defined,  please define on company information!")

        account_cash = self.env.user.company_id.account_cash_id
        if not account_cash:
            raise ValidationError("Account Cash not defined,  please define on company information!")

        vals = {}
        vals.update({'name': number})
        vals.update({'journal_id': jurnal_endofday.id})
        vals.update({'date': self.date_endofday})
        vals.update({'line_ids': [(0, 0,{
            'move_id': self.id,
            'account_id': account_company.id,
            'name': label,
            'debit': 0.0,
            'quantity': 0.0,
            'credit': self.balance,
            'date_maturity': self.date_endofday,
        }), (0, 0, {
            'move_id': self.id,
            'account_id': account_cash.id,
            'name': label,
            'debit': self.balance,
            'quantity': 0.0,
            'credit': 0.0,
            'date_maturity': self.date_endofday,
        })] })

        jurnal_entrie = jurnal_entrie_obj.create(vals)

        if not jurnal_entrie:
            raise ValidationError("Error Creating Jurnal")

        for row in self:
            args = [('date', '=', row.date_endofday)]
            res = self.env['savings.trans'].search(args).write({'state': 'posted'})


    @api.one
    def trans_post(self):
        # for row in self:
        args = [('date', '=', self.date_endofday),('state', '=', 'paid')]
        res = self.env['savings.trans'].search(args)
        if res:
            self.generate_trans_post_jurnal()
            self.state = "posted"
        else:
            raise ValidationError("You can not posted because state not paid!")


    @api.one
    def unlink(self):
        for endofday in self:
            if endofday.state == 'posted':
                raise ValidationError("You can not posted because state not paid!")
        return super(EndOfDay, self).unlink()

    @api.one
    def trans_re_open(self):
        for row in self:
            args = [('date', '=', row.date_endofday)]
            res = self.env['savings.trans'].search(args).write({'state': 'paid'})
        self.state = "new"  # pindah state ke new

    @api.one
    def generate_saving_trans(self):
        for row in self:
            args = [('date', '=', row.date_endofday)]
            res = self.env['savings.trans'].search(args).write({'endofday_id': row.id})

    @api.model
    def create(self, vals):                                                     # Di jalankan ketika Create data baru , sedangkan write(self, vals) dijalankan ketika edit data
        vals['endofday'] = self.env['ir.sequence'].next_by_code('end.of.day')
        res = super(EndOfDay, self).create(vals)                                # Super berfungsi memanggil model ketika eksekusi create
        res.generate_saving_trans()                                             # Menjalankan generate_saving_trans()
        return res

    endofday = fields.Char(string="End Of Day ID", readonly=True)
    date_endofday = fields.Date(string="Date End Of Day", )
    balance = fields.Float(string="Balance", compute='calculate_total_balance', readonly=True)
    savings_list_id = fields.One2many(comodel_name="savings.trans", inverse_name="endofday_id", string="Saving Trans ID")
    state = fields.Selection(string="State", selection=[('new', 'New'), ('posted', 'Posted'), ], default='new', required=True,)