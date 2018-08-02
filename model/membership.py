from odoo import api, fields, models


class Membership(models.Model):
    _inherit = 'res.partner'

    date_today = fields.Datetime.now
    debit_val = 300000
    credit_val = 0.00

    vals = {
        'date' : date_today,
        'debit' : debit_val,
        'credit' : credit_val,
    }

    @api.multi
    def btn_confirm(self):
        record = self.env['savings.trans'].create(vals)

    states_member = fields.Selection(string="State", selection=[('draft', 'Draft'), ('in_progress', 'In Progress'), ('active', 'Active'), ('done', 'Done')], required=True, default='draft')
    active_members = fields.Boolean(string="Active Member", )

class Termination(models.Model):
    _name = 'member.termination'
    _rec_name = 'termination_id'
    _description = 'Member Termination'

    termination_id = fields.Char(string="Termination ID", required=True, )
    member_id = fields.Many2one(comodel_name="res.partner", string="Member ID", required=True, )
    descrip = fields.Text(string="Description", required=False, )

