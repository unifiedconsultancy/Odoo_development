from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'
    _sql_constraints = [
        ("no_negative_value_downpayment", "CHECK(down_payment>=0)", "The down payment amount cannot be negative."),
        ("no_negative_value_loanpayment", "CHECK(loan_amount>0)", "The loan amount cannot be negative or ZERO."),
        ("unique_application_name", "UNIQUE(name)","The application name cannot be duplicated."),
    ]
    _order = 'date_application desc'

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
    loan_amount = fields.Monetary(compute="_compute_loan_amount",
                                  inverse="_inverse_loan_amount",
                                 currency_field="currency_id",
                                  store=True)
    loan_term = fields.Integer(string="Loan Term (Months)",
                               required=True,
                               default=36)
    reject_reason = fields.Text(copy=False)
    state = fields.Selection(selection=[
            ('draft', 'New'),
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
    document_ids = fields.One2many(comodel_name='loan.application.document',
                                   inverse_name='application_id')


    #Computed Fields
    partner_id = fields.Many2one(related="sale_order_id.partner_id")
    salesperson_id = fields.Many2one(related="sale_order_id.user_id")
    sale_order_total = fields.Monetary(related="sale_order_id.amount_total", string="Sale Order Total")
    document_count = fields.Integer(compute="_compute_document_count")
    ready_document_count = fields.Integer(compute="_compute_ready_document_count")

    @api.depends('sale_order_total','down_payment')
    def _compute_loan_amount(self):
        for loan in self:
            loan.loan_amount = loan.sale_order_total - loan.down_payment

    def _inverse_loan_amount(self):
        for loan in self:
            loan.down_payment = loan.sale_order_total - loan.loan_amount

    @api.depends('document_ids')
    def _compute_document_count(self):
        for loan in self:
            loan.document_count = len(loan.document_ids)
            loan.ready_document_count = len(loan.document_ids.filtered(lambda r: r.state == 'accepted'))

    #Constraints
    @api.constrains('down_payment')
    def _check_down_payment(self):
        for loan in self:
            if loan.sale_order_total <= (loan.down_payment):
                raise ValidationError(_("Down payment cannot be greater or equal to the Sales Total"))

    #Action
    def action_send(self):
        self.ensure_one()
        if self.document_count > self.ready_document_count:
            raise UserError(_("You are missing some documents."))
        self.state = 'sent'
        self.date_application = fields.Date().today()

    def action_approve(self):
        self.ensure_one()
        if self.state != "sent":
            raise UserError(_("You cannot approve the document without sending documenation first."))
        self.state = 'approved'
        self.date_application = fields.Date().today()

    def action_reject(self):
        self.ensure_one()
        if self.state != "rejected":
            raise UserError(_("You are reject the signed documents."))
        self.state = 'rejected'
        self.date_application = fields.Date().today()


    def action_accepted(self):
        self.ensure_one()
        if self.state == 'signed':
            raise UserError("You can not reject a signed Document.")
        self.state = 'rejected'
        self.date_rejection = fields.Date.today()
        return True