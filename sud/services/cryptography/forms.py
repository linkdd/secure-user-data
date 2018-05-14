from wtforms.validators import DataRequired
from wtforms import Form, StringField


class EncryptionForm(Form):
    key = StringField('Key', [DataRequired()])
    content = StringField('Data', [DataRequired()])


class KeyChangeForm(Form):
    new_key = StringField('New Key', [DataRequired()])
    old_key = StringField('Old Key', [DataRequired()])
    content = StringField('Data', [DataRequired()])
