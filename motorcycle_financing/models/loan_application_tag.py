from odoo import models, fields, api

class LoanApplicationTag(models.Model):
    _name = 'loan.application.tag'
    _description = 'Loan Application Tag'

    name = fields.Char(required=True)
    color = fields.Integer(default=1)