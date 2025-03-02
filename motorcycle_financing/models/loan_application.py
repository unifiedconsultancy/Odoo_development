from odoo import models, fields, api

class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

    name = fields.Char('Application Number', required=True)
    currency_id = fields.Many2one(comodel_name='res.currency',
                                  default=lambda self:self.env.company.currency_id.id)
    date_application = fields.Date(string="Applied On",
                                   copy=False)
    date_approval = fields.Date(string="Approval On",
                                readonly=True,
                                copy=False)
    date_rejection = fields.Date(string="Rejected On",
                                 readonly=True,
                                 copy=False)
    date_signed = fields.Date(string="Signed On",
                              readonly=True,
                              copy=False)
    down_payment = fields.Monetary(currency_field="currency_id")
    interest_rate = fields.Float(string="Interest Rate %",
                                 digits=(5,2))
    loan_amount = fields.Monetary(currency_field="currency_id",
                                  required=True)
    loan_term = fields.Integer(string="Loan Term (Months)",
                               required=True,
                               default=36)
    reject_reason = fields.Text(copy=False)
    state = fields.Selection(selection=[
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('reviewed', 'Credit Check'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('signed', 'Signed'),
            ('cancel', 'Cancelled')],
        default='draft',
        copy=False)
    notes = fields.Html(copy=False)

    #Relational Fields
    sale_order_id = fields.Many2one('sale.order')
    product_id = fields.Many2one(comodel_name='product.product')
    tag_ids = fields.Many2many(comodel_name='loan.application.tag')
    document_ids = fields.One2many(comodel_name='loan.application.document', inverse_name='application_id')