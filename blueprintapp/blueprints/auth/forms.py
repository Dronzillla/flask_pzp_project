from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    ValidationError,
    HiddenField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from blueprintapp.blueprints.auth.models import User
from blueprintapp.utils.utilities import auth_is_valid_password


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username already in use.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email already registered.")

    def validate_password(self, password):
        if not auth_is_valid_password(password=password.data):
            raise ValidationError(
                "Password must be at least 8 characters long, must containt at least 1 lower and 1 upper case letters, 1 digit and 1 special symbol !@#$%^&*()-_=+[{]};:'\",<.>/?"
            )


class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    new_password2 = PasswordField(
        "Repeat New Password", validators=[DataRequired(), EqualTo("new_password")]
    )
    submit = SubmitField("Update Password")

    def validate_new_password(self, new_password):
        if not auth_is_valid_password(password=new_password.data):
            raise ValidationError(
                "Password must be at least 8 characters long, must contain at least 1 lower and 1 upper case letters, 1 digit and 1 special symbol !@#$%^&*()-_=+[{]};:'\",<.>/?"
            )

    def validate_current_password(self, current_password):
        # Check if current password is correct
        user = current_user
        if not user.check_password(current_password.data):
            raise ValidationError("Current password is incorrect.")


class ConfirmDeleteForm(FlaskForm):
    user_id = HiddenField("User ID")
    submit = SubmitField("Yes")
