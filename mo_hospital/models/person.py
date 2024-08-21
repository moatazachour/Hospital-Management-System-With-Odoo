from odoo import api, fields, models, _

class HospitalPerson(models.Model):
    _name = "hospital.person"
    _inherit = "mail.thread"
    _description = "Person Record"

    name = fields.Char(string="Name", required=True, tracking=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender", tracking=True)

    _sql_constraints = [
        ('unique_patient_name', 'unique (name)', "Name must be unique!")
    ]