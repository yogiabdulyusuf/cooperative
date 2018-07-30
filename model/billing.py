from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning


class BillingPeriode(models.Model):
    _name = 'billing.periode'

    name = fields.Integer('Year', required=True)


class BillingPeriodeLine(models.Model):
    _name = 'billing.periode.line'

    name = fields.Integer('Month', required=True , readonly=True)
    billing_id = fields.Many2one('billing.periode','Periode #', readonly=True)
    start_date = fields.Date('Start Date', required=True, readonly=True)
    end_date = fields.Date('End Date', required=True, readonly=True)
    state = fields.Selection([('open','Open'),('done','Close')],'Status', default='open', readonly=True)
