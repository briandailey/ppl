from wtforms import Form, TextField, TextAreaField

class ProfileForm(Form):
    name = TextField()
    bio = TextAreaField()
    location = TextField()
    url = TextField()
    twitter = TextField()
    github_name = TextField()
