from odoo import http
from odoo.http import request


class Hospital(http.Controller):

    @http.route("/hospital/add_patient", type="http", auth="user", website=True)
    def add_patient_form(self, **kwargs):
        return request.render("mo_hospital.add_patient_form_template")

    @http.route("/hospital/create_patient", type="http", auth="user", methods=["POST"], website=True)
    def create_patient(self, **post):
        if post.get("name") and post.get("gender"):
            request.env["hospital.patient"].sudo().create({
                "name": post["name"],
                "gender": post["gender"],
            })
            request.session["message"] = "Patient added successfully!"
            return request.redirect("/hospital/add_patient")

        request.session["message"] = "Failed to add patient!"
        return request.redirect("/hospital/add_patient")

    # @http.route('/hospital/patient/', website=True, auth='public')
    # def hospital_patient(self, **kw):
    #     patients = request.env["hospital.patient"].sudo().search([])
    #     # print("patients---->", patients)
    #     return request.render("mo_hospital.patients_page", {
    #         "patients": patients
    #     })

