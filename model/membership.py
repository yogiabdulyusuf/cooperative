from odoo import api, fields, models

#_logger = logging.getLogger(__name__)

STATES = [('draft', 'Draft'), ('in_progress', 'In Progress'), ('active', 'Active'), ('done', 'Done')]

class Membership(models.Model):
    _inherit = 'res.partner'

    states               = fields.Selection(string="State", selection=STATES, required=True, default='draft')
    active_members       = fields.Boolean(string="Active Member", )


class Termination(models.Model):
    _name = 'member.termination'
    _rec_name = 'termination_id'
    _description = 'Member Termination'

    termination_id = fields.Char(string="Termination ID", required=True, )
    member_id = fields.Many2one(comodel_name="res.partner", string="Member ID", required=True, )
    descrip = fields.Text(string="Description", required=False, )

