from odoo import api, fields, models, _


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = 'mail.thread'
    _description = "Appointment Records"

    patient_id = fields.Many2one("hospital.patient", string="Patient", tracking=True)
    ref = fields.Char(string="Reference", default=lambda self: _('New'))
    gender = fields.Selection(related="patient_id.gender")
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", tracking=True)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)
    appointment_time = fields.Datetime(string="Appointment Time", default=fields.Datetime.now)
    pharmacy_line_ids = fields.One2many("appointment.pharmacy.lines", "appointment_id", string="Pharmacy Lines")
    state = fields.Selection([
        ("draft", "Draft"),
        ("in_consultation", "In Consultation"),
        ("done", "Done"),
        ("cancel", "Cancelled")], default="draft", string="Status", required=True, tracking=True
    )

    def name_get(self):
        res = []
        for rec in self:
            name = f"{rec.ref}"
            res.append((rec.id, name))
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["ref"] = self.env["ir.sequence"].next_by_code("hospital.appointment")
        return super(HospitalAppointment, self).create(vals_list)

    def action_in_consultation(self):
        for rec in self:
            rec.state = "in_consultation"

    def action_cancel(self):
        action = self.env.ref("mo_hospital.action_cancel_appointment").read()[0]
        action['context'] = {'default_appointment_id': self.id}
        return action

class HospitalPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one("product.product", required=True)
    price_unit = fields.Float(related="product_id.list_price")
    qty = fields.Integer(string="Quantity", default=1)
    appointment_id = fields.Many2one("hospital.appointment", string="Appointment")


