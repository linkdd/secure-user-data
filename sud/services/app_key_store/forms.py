from wtforms.validators import Length, DataRequired
from wtforms import Form, StringField


class ApplicationForm(Form):
    appid = StringField('Application ID', [
        Length(min=36, max=36),
        DataRequired()
    ])


class ChangeKeyForm(Form):
    appid = StringField('Application ID', [
        Length(min=36, max=36),
        DataRequired()
    ])
    key = StringField('New Application Access Key', [DataRequired()])
