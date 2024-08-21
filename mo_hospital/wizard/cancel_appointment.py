from odoo import api, fields, models


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    appointment_id = fields.Many2one("hospital.appointment", string="Appointment")
    reason = fields.Text(string="Reason")

    def action_cancel(self):
        if self.appointment_id:
            self.appointment_id.state = "cancel"




# class TestInherit(models.Model):
#     _inherit = "hospital.patient"
#
#     test = fields.Char(string="Appointment")
