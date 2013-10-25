from wtforms import Form, TextField, TextAreaField

class GroupForm(Form):
    name = TextField()
    description = TextAreaField()
    meeting_info = TextAreaField()
    url = TextField()
    mailing_list = TextField()

