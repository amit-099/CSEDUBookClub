from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField
from wtforms.validators import DataRequired, length, Email, EqualTo


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username',
                           validators=[DataRequired(), length(min=3, max=20)])
    contact = StringField('Contact No.', validators=[DataRequired(), length(min=11)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class Reset(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')


class Grades(FlaskForm):
    bangla = FloatField('Bangla', validators=[DataRequired()])
    english = FloatField('English', validators=[DataRequired()])
    math = FloatField('Math', validators=[DataRequired()])
    physics = FloatField('Physics', validators=[DataRequired()])
    chemistry = FloatField('Chemistry', validators=[DataRequired()])
    biology = FloatField('Biology', validators=[DataRequired()])
    ssc = FloatField('SSC', validators=[DataRequired()])
    hsc = FloatField('HSC', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddBook(FlaskForm):
    name = StringField('Book Name', validators=[DataRequired()])
    writer = StringField('Writer\'s Name', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    availability = StringField('Availability', validators=[DataRequired()])
