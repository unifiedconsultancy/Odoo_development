from odoo import models, fields, api

class LoanApplicationTag(models.Model):
    _name = 'loan.application.tag'
    _description = 'Loan Application Tag'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer(default=1)
