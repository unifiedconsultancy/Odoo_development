from odoo import models, fields, api

class LoanApplicationDocumentType(models.Model):
    _name = 'loan.application.document.type'
    _description = 'Loan Application Document Type'
    _order = 'name'

    name = fields.Char()
    active = fields.Boolean(default=True)
    document_number = fields.Integer(default=1)

