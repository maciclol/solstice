from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError, URL
from solstice.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username unavailable.")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email in use.")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')

class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=25)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Change Profile Picture', validators=[FileAllowed(["jpg", "png", "gif"])])
    submit = SubmitField('SAVE CHANGES')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username unavailable.")

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Email in use.")

class ProjectForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired(), Length(min=10, max=300)])
    survey = StringField("Survey Link", validators=[DataRequired(), URL(require_tld=True)])
    submit = SubmitField('CREATE POST')

class PostForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired(), Length(min=10, max=300)])
    #survey = StringField("Survey Link", validators=[DataRequired(), URL(require_tld=True)])
    submit = SubmitField('CREATE POST')
