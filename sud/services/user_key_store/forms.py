from wtforms.validators import Length, DataRequired
from wtforms import Form, StringField


class ApplicationForm(Form):
    appid = StringField('Application ID', [
        Length(min=36, max=36),
        DataRequired()
    ])


class ForgetForm(Form):
    appid = StringField('Application ID', [
        Length(min=36, max=36),
        DataRequired()
    ])
    user_id = StringField('User ID', [
        Length(min=36, max=36),
        DataRequired()
    ])
