from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=16, message="Password must be atleast 8 characters long")])
    confirm_password = PasswordField(
        "Password", validators=[DataRequired(), EqualTo("password", message='Passwords must match')]
    )
    submit = SubmitField("Register")

class ConfirmUser(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    submit = SubmitField("Confirm")