from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = 'hospital.person'
    # _inherits = {"hospital.patient": "related_patient_id"} Only inherit fields
    _description = "Doctor Records"
    _rec_name = "ref"

    ref = fields.Char(string="Reference", default=lambda self: _('New'))
    related_user = fields.Many2one("res.users", string="Related User")
    # related_patient_id = fields.Many2one("hospital.pat ient", string="Related Patient ID")


    def name_get(self):
        res = []
        for rec in self:
            name = f"{rec.ref} - {rec.name}"
            res.append((rec.id, name))
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["ref"] = self.env["ir.sequence"].next_by_code("hospital.doctor")
        return super(HospitalDoctor, self).create(vals_list)
