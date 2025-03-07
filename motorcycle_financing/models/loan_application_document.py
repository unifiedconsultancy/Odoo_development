from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class LoanApplicationDocument(models.Model):
    _name = 'loan.application.document'
    _description = 'Loan Application Document'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    application_id = fields.Many2one(comodel_name='loan.application')
    attachment = fields.Binary()
    type  = fields.Many2one(comodel_name='loan.application.document.type')
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),],
        required=True, default='new')

    def doc_status_accept(self):
        self.write({'state': 'accepted'})

    def doc_status_reject(self):
        self.write({'state': 'rejected'})