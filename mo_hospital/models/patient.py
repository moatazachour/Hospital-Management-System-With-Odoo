from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = 'hospital.person'
    _description = "Patient Records"

    date_of_birth = fields.Date(string="Date Of Birth", required=True, tracking=True)
    age = fields.Integer(string="Age", compute="_compute_age")
    is_child = fields.Boolean(string="Is Child ?", tracking=True)
    notes = fields.Text(string="Notes")
    dept_amount = fields.Float(string="Dept Amount", tracking=True)
    capitalized_name = fields.Char(string="Capitalized Name", compute="_compute_capitalized_name")
    next_appointment_date = fields.Date(string="Next Appointment", tracking=True)

    ref = fields.Char(string="reference", default=lambda self: _('New'))

    doctor_id = fields.Many2one("hospital.doctor", string="Doctor")
    tag_ids = fields.Many2many("res.partner.category", "hospital_patient_tag_rel", "patient_id", "tag_id",
                               string="Tags")
    appointment_count = fields.Integer(string="Appointment Count", compute="_compute_appointment_count", )
    appointment_ids = fields.One2many("hospital.appointment", "patient_id", string="Appointments")

    _sql_constraints = [
        ('unique_patient_name', 'unique (name)', "Name must be unique!")
    ]

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env["hospital.appointment"].search_count([("patient_id", "=", rec.id)])
        # appointment_group = self.env["hospital.appointment"].read_group(domain=[],
        #                                                                 fields=["patient_id"], groupby=["patient_id"])
        # for appointment in appointment_group:
        #     patient_id = appointment.get("patient_id")[0]
        #     patient_rec = self.browse(patient_id)
        #     patient_rec.appointment_count = appointment["patient_id_count"]
        #     self -= patient_rec
        # self.appointment_count = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["ref"] = self.env["ir.sequence"].next_by_code("hospital.patient")
        return super(HospitalPatient, self).create(vals_list)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1

    @api.depends('name')
    def _compute_capitalized_name(self):
        for rec in self:
            if rec.name:
                rec.capitalized_name = rec.name.upper()
            else:
                rec.capitalized_name = ''

    @api.constrains('is_child', 'age')
    def _check_child_age(self):
        for rec in self:
            if rec.is_child and rec.age == 0:
                raise ValidationError(_("Age has to be recorded !"))

    @api.onchange('age')
    def _onchange_age(self):
        if self.age <= 10:
            self.is_child = True
        else:
            self.is_child = False

    def action_view_appointments(self):
        return {
            'name': _('Appointments'),
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form,calendar',
            'context': {'default_patient_id': self.id},
            'domain': [('patient_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }
