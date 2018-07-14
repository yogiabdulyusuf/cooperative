from odoo import api, fields, models

class Savings(models.Model):
    _name = 'savings.type'
    _rec_name = 'name_savings_type'

    name_savings_type = fields.Char(string="Savings Type", required=True, )


class SavingInterest(models.Model):
    _name = 'savings.interest'
    _rec_name = 'type_interest'
    _description = 'Interest'

    type_interest = fields.Char(string="Type of Interest", required=True, )
    value_interest = fields.Float(string="Value of Interest",  required=True, )
