from odoo import api, fields, models

_logger = logging.getLogger(__name__)

STATES = [('draft', 'Draft'), ('in_progress', 'In Progress'), ('active', 'Active'), ('done', 'Done')]

class Membership(models.Model):
    _inherit = 'res.partner'

    active_member       = fields.Boolean(string="Active Member", )
    state               = fields.Selection(string="", selection=STATES, required=True, default='draft')