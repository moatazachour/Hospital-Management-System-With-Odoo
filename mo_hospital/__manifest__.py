{
    'name': 'Hospital Management System',
    'author': 'Moataz',
    'website': 'www.odoomoataz.tech',
    'summary': 'Odoo 16 Development',
    'depends': ['mail','product','website','base'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'wizard/cancel_appointment_view.xml',
        'views/patient.xml',
        'views/doctor.xml',
        'views/appointment.xml',
        'views/add_patient_form_template.xml',
        'reports/patient_card.xml',
        'reports/report.xml',
        'views/menu.xml'
    ]
}

