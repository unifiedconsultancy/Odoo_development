from odoo import models, fields, api

class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

    name = fields.Char('Application Number', required=True)
    currency_id = fields.Many2one(comodel_name='res.currency')
    date_application = fields.Date(string="Applied On", readonly=True)
    date_approval = fields.Date(string="Approval On", readonly=True)
    date_rejection = fields.Date(string="Rejected On", readonly=True)
    date_signed = fields.Date(string="Signed On", readonly=True)
    down_payment = fields.Monetary(currency_field="currency_id")
    interest_rate = fields.Float(string="Interest Rate %", digits=(5,4))
    loan_amount = fields.Monetary(currency_field="currency_id")
    loan_term = fields.Integer(string="Loan Term (Months)", required=True, default=36)
    reject_reason = fields.Text()
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('reviewed', 'Credit Check'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('signed', 'Signed'),
        ('cancel', 'Cancelled')],default='draft')
    notes = fields.Html()