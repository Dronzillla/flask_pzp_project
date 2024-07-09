from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField


class ConfirmDeleteForm(FlaskForm):
    user_id = HiddenField("User ID")
    submit = SubmitField("Yes")
