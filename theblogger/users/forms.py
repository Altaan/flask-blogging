from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from theblogger.models import User


class LoginForm(FlaskForm):  # This class is used to create the log in form
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):  # This class is used to register new users
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo(
        "pass_confirm", message="Passwords must match!")])
    pass_confirm = PasswordField(
        "Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register!")

    # checking if the email is already used by another user
    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError("Email is already in use!")

    # checking if the username is already in use
    def validate_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError("Username is already in use!")


# This class is used to allow the users to update their profiles
class UpdateUserForm(FlaskForm):
    email = StringField("Change Email", validators=[Email()])
    username = StringField("Change Username")
    # Setting the allowed file to be uploaded to only jpg and png
    picture = FileField("Update Profile Picture", validators=[
                        FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")

    # checking if the email is already used by another user
    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError("Email is already in use!")

    # checking if the username is already in use
    def validate_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError("Username is already in use!")
