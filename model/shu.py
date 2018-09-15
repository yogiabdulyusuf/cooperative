from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class shuAllocated(models.Model):
    _name = 'shu.allocated'
    _rec_name = 'name'
    _description = 'SHU Allocated'

    name = fields.Char(string="Name", required=True, )
    percentage = fields.Float(string="Percentage %",  required=True, )