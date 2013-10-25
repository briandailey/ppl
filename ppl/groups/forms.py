from wtforms import Form, TextField, TextAreaField, validators

class GroupForm(Form):
    name = TextField('Group Name', [validators.Required()])
    description = TextAreaField()
    meeting_info = TextAreaField()
    url = TextField()
    mailing_list = TextField()

