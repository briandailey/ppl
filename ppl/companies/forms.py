from wtforms import Form, TextField, TextAreaField, validators

class CompanyForm(Form):
    name = TextField('Company Name', [validators.Required()])
    url = TextField()
    address = TextAreaField()
    description = TextAreaField()
    location = TextField()
    email = TextField()

